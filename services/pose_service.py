import cv2
import mediapipe as mp
import numpy as np
import base64
import time
import logging
from services.angle_service import get_joint_angles, extract_landmark

logger = logging.getLogger(__name__)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Map joint names to MediaPipe landmark indices for coloring
_JOINT_LANDMARK_MAP = {
    'left_knee': mp_pose.PoseLandmark.LEFT_KNEE,
    'right_knee': mp_pose.PoseLandmark.RIGHT_KNEE,
    'left_elbow': mp_pose.PoseLandmark.LEFT_ELBOW,
    'right_elbow': mp_pose.PoseLandmark.RIGHT_ELBOW,
    'left_shoulder': mp_pose.PoseLandmark.LEFT_SHOULDER,
    'right_shoulder': mp_pose.PoseLandmark.RIGHT_SHOULDER,
    'left_hip': mp_pose.PoseLandmark.LEFT_HIP,
    'right_hip': mp_pose.PoseLandmark.RIGHT_HIP,
}


class PoseService:
    def __init__(self, config):
        self.config = config
        self.pose = mp_pose.Pose(
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE,
            model_complexity=1,
            smooth_landmarks=True,
        )
        self.frame_times = []
        self.fps = 0

    def extract_pose(self, frame):
        h, w = frame.shape[:2]
        t_start = time.time()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = self.pose.process(rgb)
        rgb.flags.writeable = True

        angles = {}
        if results.pose_landmarks:
            angles = get_joint_angles(results.pose_landmarks.landmark, w, h)
            
        return results, angles, t_start

    def draw_and_encode(self, frame, results, angles, posture_ok=True, joint_status=None, t_start=None, feedback=''):
        h, w = frame.shape[:2]
        drawn = frame.copy()

        if results and results.pose_landmarks:
            self._draw_skeleton(drawn, results.pose_landmarks, w, h, posture_ok, joint_status)
            self._draw_angles(drawn, results.pose_landmarks, w, h, angles, joint_status)
        
        # Overlay border glow
        border_color = (0, 220, 80) if posture_ok else (0, 60, 220)
        cv2.rectangle(drawn, (4, 4), (w - 4, h - 4), border_color, 3)

        if feedback:
            # Draw visual feedback overlay if provided
            fb_color = (0, 255, 0) if posture_ok else (0, 0, 255)
            fb_text = f"GOOD FORM" if posture_ok else f"BAD FORM: {feedback}"
            (fw, fh), _ = cv2.getTextSize(fb_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
            cv2.rectangle(drawn, (w//2 - fw//2 - 10, 10), (w//2 + fw//2 + 10, 10 + fh + 20), (0,0,0), -1)
            cv2.putText(drawn, fb_text, (w//2 - fw//2, 10 + fh + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, fb_color, 2, cv2.LINE_AA)

        # FPS counter
        if t_start:
            t_end = time.time()
            self.frame_times.append(t_end - t_start)
            if len(self.frame_times) > 20:
                self.frame_times.pop(0)
            self.fps = round(1.0 / (sum(self.frame_times) / len(self.frame_times))) if self.frame_times else 0

        cv2.putText(drawn, f"FPS: {self.fps}", (10, h - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

        # Encode to JPEG → base64
        _, jpeg = cv2.imencode('.jpg', drawn, [cv2.IMWRITE_JPEG_QUALITY, 80])
        b64 = base64.b64encode(jpeg.tobytes()).decode('utf-8')

        return b64

    def _draw_skeleton(self, frame, landmarks, w, h, posture_ok, joint_status=None):
        """Draw skeleton with per-joint GREEN/RED coloring."""
        connections = mp_pose.POSE_CONNECTIONS
        lm = landmarks.landmark

        # ── 1. Draw skeleton lines in WHITE ──
        for conn in connections:
            a_idx, b_idx = conn
            a = lm[a_idx]
            b = lm[b_idx]
            if a.visibility > 0.5 and b.visibility > 0.5:
                ax, ay = int(a.x * w), int(a.y * h)
                bx, by = int(b.x * w), int(b.y * h)
                # Glow effect: thick colored line + thin white overlay
                cv2.line(frame, (ax, ay), (bx, by), (80, 80, 80), 4, cv2.LINE_AA)
                cv2.line(frame, (ax, ay), (bx, by), (255, 255, 255), 1, cv2.LINE_AA)

        # ── 2. Build per-landmark color map ──
        landmark_colors = {}
        if joint_status:
            for joint_name, status in joint_status.items():
                if joint_name in _JOINT_LANDMARK_MAP:
                    idx = _JOINT_LANDMARK_MAP[joint_name].value
                    if status['correct']:
                        landmark_colors[idx] = (0, 255, 0)   # GREEN
                    else:
                        landmark_colors[idx] = (0, 0, 255)    # RED

        # Default color for untracked joints
        default_color = (0, 255, 200) if posture_ok else (0, 140, 255)

        # ── 3. Draw joints with per-joint coloring ──
        for i, lmk in enumerate(lm):
            if lmk.visibility > 0.5:
                cx, cy = int(lmk.x * w), int(lmk.y * h)
                
                # Highlight logic: RED joints are 12px, GREEN are 8px, default are 5px
                if i in landmark_colors:
                    color = landmark_colors[i]
                    radius = 12 if color == (0, 0, 255) else 8
                else:
                    color = default_color
                    radius = 5
                    
                thickness = -1  # filled
                cv2.circle(frame, (cx, cy), radius, color, thickness, cv2.LINE_AA)
                # White outline for contrast
                cv2.circle(frame, (cx, cy), radius + 2, (255, 255, 255), 1, cv2.LINE_AA)

    def _draw_angles(self, frame, landmarks, w, h, angles, joint_status=None):
        """Draw angle values near joints with color indicating correctness."""
        lm = landmarks.landmark
        L = mp_pose.PoseLandmark

        angle_positions = {
            'left_knee': L.LEFT_KNEE,
            'right_knee': L.RIGHT_KNEE,
            'left_elbow': L.LEFT_ELBOW,
            'right_elbow': L.RIGHT_ELBOW,
            'left_shoulder': L.LEFT_SHOULDER,
            'right_shoulder': L.RIGHT_SHOULDER,
        }

        for key, landmark_idx in angle_positions.items():
            if key in angles:
                lmk = lm[landmark_idx]
                if lmk.visibility > 0.5:
                    cx, cy = int(lmk.x * w), int(lmk.y * h)
                    text = f"{int(angles[key])}\u00b0"

                    # Color based on joint correctness
                    if joint_status and key in joint_status:
                        text_color = (100, 255, 100) if joint_status[key]['correct'] else (100, 100, 255)
                    else:
                        text_color = (100, 255, 180)

                    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    cv2.rectangle(frame, (cx + 5, cy - th - 4), (cx + 5 + tw + 4, cy + 2),
                                  (0, 0, 0), -1)
                    cv2.putText(frame, text, (cx + 7, cy - 2),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

    def release(self):
        self.pose.close()
