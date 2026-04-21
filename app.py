import cv2
import time
import threading
import logging
import functools

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_socketio import SocketIO, emit

from config import Config
from database.db import (
    init_db, save_session, get_session_history, log_rep, get_stats,
    create_user, verify_user, get_user_by_id
)
from services.pose_service import PoseService
from services.exercise_service import ExerciseTracker, EXERCISES, feedback_map
from services.feedback_service import FeedbackService
from utils.helpers import generate_session_id, setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ── Global state ──────────────────────────────────────────────────────────────
camera = None
pose_service = None
exercise_tracker = None
feedback_service = FeedbackService(audio_enabled=Config.AUDIO_ENABLED, cooldown=Config.AUDIO_COOLDOWN)

session_active = False
is_paused = False
current_session_id = None
session_start_time = None
stream_thread = None
stop_stream = threading.Event()

# ── Init ──────────────────────────────────────────────────────────────────────
init_db()

# ── Auth helpers ──────────────────────────────────────────────────────────────
def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def get_current_user():
    uid = session.get('user_id')
    if uid:
        return get_user_by_id(uid)
    return None

# ── Auth routes ───────────────────────────────────────────────────────────────
@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    phone = data.get('phone', '').strip()
    age = data.get('age')
    dob = data.get('dob', '').strip()
    height = data.get('height')
    weight = data.get('weight')

    if not name or not email or not password:
        return jsonify({'error': 'Name, email, and password are required'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    try:
        age = int(age) if age else None
        height = float(height) if height else None
        weight = float(weight) if weight else None
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid numeric values'}), 400

    ok, msg = create_user(name, email, password, phone, age, dob, height, weight)
    if ok:
        user = verify_user(email, password)
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
        return jsonify({'message': msg}), 201
    return jsonify({'error': msg}), 400

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = verify_user(email, password)
    if user:
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        return jsonify({'message': 'Login successful', 'name': user['name']})
    return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'message': 'Logged out'})

@app.route('/api/me')
def api_me():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'not logged in'}), 401
    return jsonify({
        'name': user['name'],
        'email': user['email'],
        'phone': user.get('phone'),
        'age': user.get('age'),
        'dob': user.get('dob'),
        'height': user.get('height'),
        'weight': user.get('weight'),
    })

# ── Page routes ───────────────────────────────────────────────────────────────
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# ── Exercise API ──────────────────────────────────────────────────────────────
@app.route('/api/start-session', methods=['POST'])
@login_required
def start_session_route():
    global camera, pose_service, exercise_tracker, session_active, is_paused
    global current_session_id, session_start_time, stream_thread, stop_stream

    data = request.get_json() or {}
    exercise_type = data.get('exercise', 'squat')

    if session_active:
        return jsonify({'error': 'Session already active'}), 400

    try:
        camera = cv2.VideoCapture(Config.CAMERA_INDEX)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, Config.FRAME_WIDTH)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.FRAME_HEIGHT)
        camera.set(cv2.CAP_PROP_FPS, Config.FPS_TARGET)

        if not camera.isOpened():
            return jsonify({'error': 'Camera not accessible'}), 500

        pose_service = PoseService(Config)
        exercise_tracker = ExerciseTracker(exercise_type)
        current_session_id = generate_session_id()
        session_start_time = time.time()
        session_active = True
        is_paused = False
        stop_stream.clear()

        stream_thread = threading.Thread(target=_stream_loop, daemon=True)
        stream_thread.start()

        logger.info(f"[Session] Started: {current_session_id} ({exercise_type})")
        return jsonify({'session_id': current_session_id, 'exercise': exercise_type})

    except Exception as e:
        logger.error(f"[Session] Start error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/end-session', methods=['POST'])
def end_session_route():
    global session_active, camera, pose_service, stop_stream

    if not session_active:
        return jsonify({'error': 'No active session'}), 400

    stop_stream.set()
    session_active = False
    time.sleep(0.3)

    summary = exercise_tracker.get_summary() if exercise_tracker else {}
    duration = int(time.time() - session_start_time) if session_start_time else 0

    user_id = session.get('user_id')
    if current_session_id and exercise_tracker:
        save_session(
            current_session_id,
            exercise_tracker.exercise_type,
            exercise_tracker.total_reps,
            exercise_tracker.correct_reps,
            duration,
            user_id=user_id
        )

    if camera:
        camera.release()
        camera = None
    if pose_service:
        pose_service.release()
        pose_service = None

    logger.info(f"[Session] Ended: {current_session_id}")
    return jsonify({**summary, 'duration': duration, 'session_id': current_session_id})

@app.route('/api/get-history')
def get_history():
    limit = request.args.get('limit', 20, type=int)
    user_id = session.get('user_id')
    return jsonify(get_session_history(limit, user_id=user_id))

@app.route('/api/stats')
def api_stats():
    user_id = session.get('user_id')
    return jsonify(get_stats(user_id=user_id))

@app.route('/api/exercises')
def api_exercises():
    return jsonify({k: {
        'name': v.get('name', 'Exercise'),
        'icon': v.get('icon', '🔹'),
        'description': v.get('description', ''),
        'category': v.get('category', 'Other'),
        'steps': v.get('steps', ''),
        'tips': v.get('tips', ''),
        'type': v.get('type', 'rep'),
    } for k, v in EXERCISES.items()})

@app.route('/api/set-exercise', methods=['POST'])
def set_exercise():
    global exercise_tracker
    data = request.get_json() or {}
    ex_type = data.get('exercise', 'squat')
    if session_active:
        exercise_tracker = ExerciseTracker(ex_type)
        logger.info(f"[Session] Switched exercise to {ex_type}")
        return jsonify({'status': 'switched', 'exercise': ex_type})
    return jsonify({'error': 'no active session'}), 400

@app.route('/api/pause-session', methods=['POST'])
def pause_session():
    global is_paused
    is_paused = not is_paused
    logger.info(f"[Session] Paused state changed to {is_paused}")
    return jsonify({'paused': is_paused})

@app.route('/api/reset-session', methods=['POST'])
def reset_session():
    if exercise_tracker:
        exercise_tracker.reset()
        logger.info("[Session] Tracker reset")
    return jsonify({'status': 'reset'})

# ── Streaming loop ────────────────────────────────────────────────────────────
def _stream_loop():
    global session_active
    logger.info("[Stream] Loop started")
    frame_count = 0
    while not stop_stream.is_set() and session_active:
        try:
            ret, frame = camera.read()
            if not ret or frame is None:
                time.sleep(0.03)
                continue

            frame_count += 1
            if frame_count % 2 != 0:
                continue

            frame = cv2.resize(frame, (640, 480))
            frame = cv2.flip(frame, 1)

            results, angles, t_start = pose_service.extract_pose(frame)
            pose_detected = bool(results and results.pose_landmarks)

            status = {}
            joint_status = None

            if not is_paused and pose_detected and exercise_tracker and angles:
                joint_status = exercise_tracker.get_joint_status(angles)
                status = exercise_tracker.update(angles)

                incorrect_joints = [v for k, v in joint_status.items() if not v['correct']]
                
                if exercise_tracker.state == 'down' or len(incorrect_joints) > 0:
                    if incorrect_joints:
                        error_code = incorrect_joints[0].get('error_code', 'good')
                        status['feedback'] = feedback_map.get(error_code, "Good form")
                        status['posture_ok'] = False
                    else:
                        status['feedback'] = "Good form"
                        status['posture_ok'] = True
                
                exercise_tracker.posture_ok = status.get('posture_ok', True)
                posture_changed = exercise_tracker.posture_changed()

                if status.get('rep_complete'):
                    log_rep(
                        current_session_id,
                        status['total_reps'],
                        status.get('posture_ok', False),
                        status.get('peak_angle', 0),
                    )

                feedback_service.give_feedback(
                    status.get('feedback', ''),
                    status.get('posture_ok', True),
                    status.get('rep_complete', False),
                    posture_changed=posture_changed,
                )
            elif is_paused and exercise_tracker:
                status = {
                    'total_reps': exercise_tracker.total_reps,
                    'correct_reps': exercise_tracker.correct_reps,
                    'posture_ok': exercise_tracker.posture_ok,
                    'feedback': 'Session paused',
                    'state': exercise_tracker.state,
                }

            b64 = pose_service.draw_and_encode(
                frame, 
                results, 
                angles, 
                posture_ok=status.get('posture_ok', True), 
                joint_status=joint_status, 
                t_start=t_start,
                feedback=status.get('feedback', '') if not status.get('posture_ok', True) else ''
            )

            socketio.emit('frame', {
                'image': b64,
                'angles': angles,
                'fps': pose_service.fps,
                'pose_detected': pose_detected,
                **status,
            })
            time.sleep(0.01)

        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(f"[Stream] Error: {e}")
            time.sleep(0.1)

    logger.info("[Stream] Loop ended")

# ── SocketIO events ───────────────────────────────────────────────────────────
@socketio.on('connect')
def on_connect():
    logger.info(f"[WS] Client connected: {request.sid}")

@socketio.on('disconnect')
def on_disconnect():
    logger.info(f"[WS] Client disconnected: {request.sid}")

if __name__ == '__main__':
    logger.info("🚀 AI-Physio starting on http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
