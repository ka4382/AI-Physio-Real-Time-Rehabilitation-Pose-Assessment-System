"""
Exercise configuration and state machine for rep counting and form validation.
Supports 24 exercises across 4 categories:
  - Core & Back
  - Lower Body
  - Upper Body & Posture
  - Mobility & Flexibility
"""

EXERCISES = {
    # ═══════════════════════════════════════════════════════════════════════════
    # CORE & BACK STRENGTH
    # ═══════════════════════════════════════════════════════════════════════════
    'bridge': {
        'name': 'Glute Bridge',
        'icon': '🌉',
        'category': 'Core & Back',
        'description': 'Glute and core activation',
        'steps': '1. Lie on your back, knees bent. 2. Push hips up squeezing glutes. 3. Lower slowly.',
        'tips': 'Keep core tight. Don\'t arch your lower back excessively.',
        'target_joint': 'left_knee',
        'down_angle': 90,
        'up_angle': 160,
        'correct_range': (140, 180),
        'feedback_down': 'Lower your hips',
        'feedback_up': 'Push hips up higher',
        'feedback_correct': 'Perfect bridge!',
        'feedback_too_shallow': 'Raise hips to full extension',
    },
    'plank': {
        'name': 'Plank',
        'icon': '🧱',
        'category': 'Core & Back',
        'description': 'Core stability hold',
        'steps': '1. Get into push-up position. 2. Hold body in a straight line. 3. Engage your core.',
        'tips': 'Don\'t let hips sag or pike up. Keep a neutral spine.',
        'type': 'hold',
        'target_joint': 'left_elbow',
        'down_angle': 160,
        'up_angle': 180,
        'correct_range': (150, 180),
        'feedback_down': 'Hold the position',
        'feedback_up': 'Keep your body straight',
        'feedback_correct': 'Great plank hold!',
        'feedback_too_shallow': 'Straighten your body',
    },
    'bird_dog': {
        'name': 'Bird Dog',
        'icon': '🐕',
        'category': 'Core & Back',
        'description': 'Balance and core strength',
        'steps': '1. Start on hands and knees. 2. Extend opposite arm and leg. 3. Return and switch sides.',
        'tips': 'Keep your back flat and move slowly.',
        'target_joint': 'left_shoulder',
        'down_angle': 20,
        'up_angle': 160,
        'correct_range': (140, 180),
        'feedback_down': 'Return to start position',
        'feedback_up': 'Extend arm and leg fully',
        'feedback_correct': 'Excellent bird dog!',
        'feedback_too_shallow': 'Extend further for full range',
    },
    'dead_bug': {
        'name': 'Dead Bug',
        'icon': '🪲',
        'category': 'Core & Back',
        'description': 'Core anti-extension',
        'steps': '1. Lie on your back, arms up. 2. Extend opposite arm and leg toward floor. 3. Return and switch.',
        'tips': 'Press lower back into the floor throughout.',
        'target_joint': 'left_knee',
        'down_angle': 90,
        'up_angle': 160,
        'correct_range': (140, 180),
        'feedback_down': 'Bring knee back up',
        'feedback_up': 'Extend leg fully',
        'feedback_correct': 'Great dead bug!',
        'feedback_too_shallow': 'Extend the leg more',
    },
    'pelvic_tilts': {
        'name': 'Pelvic Tilts',
        'icon': '🔄',
        'category': 'Core & Back',
        'description': 'Lower back mobility',
        'steps': '1. Lie on your back, knees bent. 2. Flatten back against floor. 3. Release and repeat.',
        'tips': 'Move slowly and breathe with each tilt.',
        'target_joint': 'left_knee',
        'down_angle': 80,
        'up_angle': 110,
        'correct_range': (75, 115),
        'feedback_down': 'Tilt pelvis back',
        'feedback_up': 'Release the tilt',
        'feedback_correct': 'Good pelvic control!',
        'feedback_too_shallow': 'Press back flat against floor',
    },
    'superman': {
        'name': 'Superman',
        'icon': '🦸',
        'category': 'Core & Back',
        'description': 'Back extension strength',
        'steps': '1. Lie face down. 2. Lift arms and legs off floor. 3. Hold, then lower.',
        'tips': 'Look at the floor to keep neck neutral.',
        'target_joint': 'left_shoulder',
        'down_angle': 20,
        'up_angle': 160,
        'correct_range': (130, 180),
        'feedback_down': 'Lower back down',
        'feedback_up': 'Lift arms and legs higher',
        'feedback_correct': 'Perfect superman!',
        'feedback_too_shallow': 'Lift higher off the ground',
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # LOWER BODY
    # ═══════════════════════════════════════════════════════════════════════════
    'squat': {
        'name': 'Squat',
        'icon': '🦵',
        'category': 'Lower Body',
        'description': 'Lower body strength',
        'steps': '1. Stand feet shoulder-width apart. 2. Lower hips back and down. 3. Return to standing.',
        'tips': 'Keep chest up and back straight. Knees over toes.',
        'target_joint': 'left_knee',
        'down_angle': 90,
        'up_angle': 160,
        'correct_range': (70, 100),
        'feedback_down': 'Bend your knees more',
        'feedback_up': 'Stand up fully',
        'feedback_correct': 'Perfect squat form!',
        'feedback_too_shallow': 'Go deeper for full range',
    },
    'wall_sit': {
        'name': 'Wall Sit',
        'icon': '🧍',
        'category': 'Lower Body',
        'description': 'Isometric leg hold',
        'steps': '1. Lean against wall. 2. Slide down until thighs are parallel. 3. Hold the position.',
        'tips': 'Keep your back flat against the wall.',
        'type': 'hold',
        'target_joint': 'left_knee',
        'down_angle': 85,
        'up_angle': 100,
        'correct_range': (80, 100),
        'feedback_down': 'Hold the sit position',
        'feedback_up': 'Slide down a bit more',
        'feedback_correct': 'Great wall sit!',
        'feedback_too_shallow': 'Get thighs to parallel',
    },
    'clamshells': {
        'name': 'Clamshells',
        'icon': '🐚',
        'category': 'Lower Body',
        'description': 'Hip abductor activation',
        'steps': '1. Lie on side, knees bent. 2. Open top knee like a clamshell. 3. Close slowly.',
        'tips': 'Keep feet together and don\'t rotate your hips.',
        'target_joint': 'left_knee',
        'down_angle': 90,
        'up_angle': 140,
        'correct_range': (120, 150),
        'feedback_down': 'Close your knees',
        'feedback_up': 'Open wider',
        'feedback_correct': 'Great clamshell!',
        'feedback_too_shallow': 'Open your knee wider',
    },
    'straight_leg_raise': {
        'name': 'Straight Leg Raise',
        'icon': '🦿',
        'category': 'Lower Body',
        'description': 'Quad and hip flexor',
        'steps': '1. Lie flat on your back. 2. Keep one leg straight, raise it up. 3. Lower slowly.',
        'tips': 'Keep the raised leg straight, don\'t bend the knee.',
        'target_joint': 'left_knee',
        'down_angle': 160,
        'up_angle': 90,
        'correct_range': (60, 100),
        'feedback_down': 'Lower your leg',
        'feedback_up': 'Raise your leg higher',
        'feedback_correct': 'Excellent leg raise!',
        'feedback_too_shallow': 'Raise leg to 90 degrees',
    },
    'calf_raises': {
        'name': 'Calf Raises',
        'icon': '🩰',
        'category': 'Lower Body',
        'description': 'Lower leg strength',
        'steps': '1. Stand near a chair for support. 2. Push up onto your toes. 3. Lower heels slowly.',
        'tips': 'Use controlled motions. Don\'t rock.',
        'target_joint': 'left_knee',
        'down_angle': 170,
        'up_angle': 180,
        'correct_range': (170, 180),
        'feedback_down': 'Lower your heels',
        'feedback_up': 'Rise up on your toes',
        'feedback_correct': 'Great calf raise!',
        'feedback_too_shallow': 'Push higher on toes',
    },
    'side_leg_lift': {
        'name': 'Side Leg Lift',
        'icon': '🏃',
        'category': 'Lower Body',
        'description': 'Hip abductor strength',
        'steps': '1. Lie on your side. 2. Lift top leg upward. 3. Lower slowly.',
        'tips': 'Keep your body in a straight line. Don\'t roll forward.',
        'target_joint': 'left_knee',
        'down_angle': 160,
        'up_angle': 100,
        'correct_range': (80, 120),
        'feedback_down': 'Lower your leg',
        'feedback_up': 'Lift your leg higher',
        'feedback_correct': 'Perfect side lift!',
        'feedback_too_shallow': 'Lift a bit higher',
    },
    'sit_to_stand': {
        'name': 'Sit-to-Stand',
        'icon': '🪑',
        'category': 'Lower Body',
        'description': 'Functional mobility',
        'steps': '1. Sit on a stable chair. 2. Stand up without using hands. 3. Sit back down slowly.',
        'tips': 'Lean forward slightly to stand. Keep knees over toes.',
        'target_joint': 'left_knee',
        'down_angle': 90,
        'up_angle': 160,
        'correct_range': (70, 100),
        'feedback_down': 'Sit all the way down',
        'feedback_up': 'Stand up fully',
        'feedback_correct': 'Great sit-to-stand!',
        'feedback_too_shallow': 'Sit all the way to the chair',
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # UPPER BODY & POSTURE
    # ═══════════════════════════════════════════════════════════════════════════
    'wall_pushup': {
        'name': 'Wall Push-Up',
        'icon': '✋',
        'category': 'Upper Body & Posture',
        'description': 'Chest and arm strength',
        'steps': '1. Stand facing a wall. 2. Place hands on wall, shoulder width. 3. Bend elbows, lean in, push back.',
        'tips': 'Keep body in a straight line. Don\'t flare elbows.',
        'target_joint': 'right_elbow',
        'down_angle': 90,
        'up_angle': 160,
        'correct_range': (70, 110),
        'feedback_down': 'Bend elbows more',
        'feedback_up': 'Push back fully',
        'feedback_correct': 'Excellent push-up!',
        'feedback_too_shallow': 'Go deeper',
    },
    'shoulder_rolls': {
        'name': 'Shoulder Rolls',
        'icon': '🔃',
        'category': 'Upper Body & Posture',
        'description': 'Shoulder mobility',
        'steps': '1. Stand tall. 2. Roll shoulders forward in circles. 3. Reverse direction.',
        'tips': 'Keep the motion smooth and controlled.',
        'type': 'motion',
        'target_joint': 'left_shoulder',
        'down_angle': 10,
        'up_angle': 40,
        'correct_range': (20, 50),
        'feedback_down': 'Roll your shoulders',
        'feedback_up': 'Keep rolling smoothly',
        'feedback_correct': 'Good shoulder rolls!',
        'feedback_too_shallow': 'Make bigger circles',
    },
    'shoulder_blade_squeeze': {
        'name': 'Shoulder Blade Squeeze',
        'icon': '🦋',
        'category': 'Upper Body & Posture',
        'description': 'Scapular retraction',
        'steps': '1. Stand or sit tall. 2. Squeeze shoulder blades together. 3. Hold 5 seconds, release.',
        'tips': 'Imagine squeezing a pencil between your shoulder blades.',
        'target_joint': 'left_shoulder',
        'down_angle': 10,
        'up_angle': 30,
        'correct_range': (15, 40),
        'feedback_down': 'Release the squeeze',
        'feedback_up': 'Squeeze blades together',
        'feedback_correct': 'Great retraction!',
        'feedback_too_shallow': 'Squeeze harder',
    },
    'chin_tucks': {
        'name': 'Chin Tucks',
        'icon': '🗣️',
        'category': 'Upper Body & Posture',
        'description': 'Neck alignment',
        'steps': '1. Sit upright. 2. Tuck chin straight back. 3. Hold 3 seconds, release.',
        'tips': 'Create a "double chin" to align your cervical spine.',
        'type': 'motion',
        'target_joint': 'left_shoulder',
        'down_angle': 10,
        'up_angle': 30,
        'correct_range': (10, 35),
        'feedback_down': 'Tuck your chin',
        'feedback_up': 'Good tuck, hold it',
        'feedback_correct': 'Perfect chin tuck!',
        'feedback_too_shallow': 'Pull chin back more',
    },
    'wall_slides': {
        'name': 'Wall Slides',
        'icon': '🧱',
        'category': 'Upper Body & Posture',
        'description': 'Shoulder mobility & upper back',
        'steps': '1. Stand with back against wall. 2. Slide arms up (goalpost position). 3. Slide back down.',
        'tips': 'Keep elbows and wrists touching the wall.',
        'target_joint': 'left_shoulder',
        'down_angle': 90,
        'up_angle': 160,
        'correct_range': (150, 180),
        'feedback_down': 'Lower elbows to 90 degrees',
        'feedback_up': 'Slide arms up higher',
        'feedback_correct': 'Excellent wall slide!',
        'feedback_too_shallow': 'Reach higher',
    },
    'pendulum_swings': {
        'name': 'Pendulum Swings',
        'icon': '🔔',
        'category': 'Upper Body & Posture',
        'description': 'Shoulder decompression',
        'steps': '1. Lean forward, let arm hang. 2. Make small circles. 3. Reverse direction.',
        'tips': 'Use body momentum, not arm muscles.',
        'type': 'motion',
        'target_joint': 'right_shoulder',
        'down_angle': 10,
        'up_angle': 40,
        'correct_range': (15, 50),
        'feedback_down': 'Let arm swing gently',
        'feedback_up': 'Keep the circles going',
        'feedback_correct': 'Good pendulum motion!',
        'feedback_too_shallow': 'Make slightly bigger circles',
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # MOBILITY & FLEXIBILITY
    # ═══════════════════════════════════════════════════════════════════════════
    'ankle_circles': {
        'name': 'Ankle Circles',
        'icon': '🦶',
        'category': 'Mobility & Flexibility',
        'description': 'Ankle joint mobility',
        'steps': '1. Sit or stand on one leg. 2. Rotate ankle in circles. 3. Reverse direction.',
        'tips': 'Make full, controlled circles.',
        'type': 'motion',
        'target_joint': 'left_knee',
        'down_angle': 160,
        'up_angle': 170,
        'correct_range': (155, 175),
        'feedback_down': 'Circle your ankle',
        'feedback_up': 'Keep circling smoothly',
        'feedback_correct': 'Good ankle mobility!',
        'feedback_too_shallow': 'Make bigger circles',
    },
    'heel_slides': {
        'name': 'Heel Slides',
        'icon': '👟',
        'category': 'Mobility & Flexibility',
        'description': 'Knee flexion recovery',
        'steps': '1. Lie on back, legs straight. 2. Slide heel toward buttock bending knee. 3. Slide back out.',
        'tips': 'Keep heel on the floor the entire time.',
        'target_joint': 'left_knee',
        'down_angle': 90,
        'up_angle': 160,
        'correct_range': (70, 100),
        'feedback_down': 'Slide heel closer',
        'feedback_up': 'Extend leg back out',
        'feedback_correct': 'Great heel slide!',
        'feedback_too_shallow': 'Bend knee more',
    },
    'cat_cow': {
        'name': 'Cat-Cow Stretch',
        'icon': '🐱',
        'category': 'Mobility & Flexibility',
        'description': 'Spinal mobility',
        'steps': '1. Start on hands and knees. 2. Arch back up (cat). 3. Drop belly down (cow). Alternate.',
        'tips': 'Move with your breath. Inhale cow, exhale cat.',
        'type': 'motion',
        'target_joint': 'left_shoulder',
        'down_angle': 20,
        'up_angle': 50,
        'correct_range': (15, 55),
        'feedback_down': 'Round your back (cat)',
        'feedback_up': 'Arch your back (cow)',
        'feedback_correct': 'Beautiful flow!',
        'feedback_too_shallow': 'Increase the range',
    },
    'childs_pose': {
        'name': "Child's Pose",
        'icon': '🧒',
        'category': 'Mobility & Flexibility',
        'description': 'Full body relaxation',
        'steps': '1. Kneel on floor. 2. Sit back on heels. 3. Extend arms forward, forehead to floor.',
        'tips': 'Breathe deeply. Let your body relax completely.',
        'type': 'hold',
        'target_joint': 'left_knee',
        'down_angle': 40,
        'up_angle': 60,
        'correct_range': (30, 70),
        'feedback_down': 'Sit back further',
        'feedback_up': 'Relax into the stretch',
        'feedback_correct': 'Perfect pose. Breathe.',
        'feedback_too_shallow': 'Sink deeper into the pose',
    },
}


feedback_map = {
    "left_shoulder_low": "Raise your left shoulder higher",
    "right_shoulder_low": "Raise your right shoulder higher",
    "elbow_not_bent": "Bend your elbow more",
    "body_leaning": "Keep your body straight",
    "neck_not_tilted": "Tilt your neck properly",
    "knee_too_shallow": "Squat deeper into your knees",
    "reach_further": "Reach your arm further",
    "shoulder_cheating": "Keep your shoulder stable",
    "bend_more": "Bend more to hit the angle",
    "extend_more": "Extend further to hit the angle",
    "good": "Good form"
}

class ExerciseTracker:
    def __init__(self, exercise_type='squat'):
        self.exercise_type = exercise_type
        self.config = EXERCISES.get(exercise_type, EXERCISES['squat'])
        self.state = 'up'  # 'up' or 'down'
        self.total_reps = 0
        self.correct_reps = 0
        self.current_rep_correct = True
        self.peak_angle = None
        self.feedback = ''
        self.rep_complete = False
        self.posture_ok = True
        self.angle_history = []
        self.last_rep_time = 0  # debounce: minimum 1s between reps
        self.min_samples = 5   # require 5 frames before evaluating
        self.frame_count = 0
        self._last_posture_state = True  # track posture state changes for audio

    def reset(self):
        self.__init__(self.exercise_type)

    def get_joint_status(self, angles):
        """Evaluate exercise-specific mechanics and return correct/incorrect joints."""
        status = {}
        name = self.exercise_type
        cfg = self.config

        # 1. Lower Body (Squats, Sit-to-Stand, Wall Sit)
        if name in ('squat', 'sit_to_stand', 'wall_sit'):
            for side in ['left', 'right']:
                knee_angle = angles.get(f'{side}_knee')
                hip_angle = angles.get(f'{side}_hip')
                
                if knee_angle is not None:
                    if self.state == 'down' and knee_angle > 100:
                        status[f'{side}_knee'] = {'correct': False, 'angle': knee_angle, 'error_code': 'knee_too_shallow'}
                    else:
                        status[f'{side}_knee'] = {'correct': True, 'angle': knee_angle, 'error_code': 'good'}
                
                if hip_angle is not None:
                    if hip_angle < 60:
                        status[f'{side}_hip'] = {'correct': False, 'angle': hip_angle, 'error_code': 'body_leaning'}
                    else:
                        status[f'{side}_hip'] = {'correct': True, 'angle': hip_angle, 'error_code': 'good'}

        # 2. Upper Body Push/Raises (Wall Pushup, Bicep Curl)
        elif name in ('wall_pushup', 'bicep_curl'):
            for side in ['left', 'right']:
                elbow_angle = angles.get(f'{side}_elbow')
                shoulder_angle = angles.get(f'{side}_shoulder')
                
                if elbow_angle is not None:
                    if self.state == 'down' and elbow_angle > 110:
                        status[f'{side}_elbow'] = {'correct': False, 'angle': elbow_angle, 'error_code': 'elbow_not_bent'}
                    else:
                        status[f'{side}_elbow'] = {'correct': True, 'angle': elbow_angle, 'error_code': 'good'}
                
                if shoulder_angle is not None and name == 'bicep_curl':
                    if shoulder_angle > 40:
                        status[f'{side}_shoulder'] = {'correct': False, 'angle': shoulder_angle, 'error_code': 'shoulder_cheating'}

        # 3. Shoulder/Neck Mobility
        elif name in ('wall_slides', 'shoulder_rolls', 'chin_tucks', 'pendulum_swings'):
            for side in ['left', 'right']:
                shoulder = angles.get(f'{side}_shoulder')
                if shoulder is not None:
                    if self.state == 'down' and shoulder < cfg['correct_range'][0] - 20: 
                        status[f'{side}_shoulder'] = {'correct': False, 'angle': shoulder, 'error_code': 'reach_further'}
                    else:
                        status[f'{side}_shoulder'] = {'correct': True, 'angle': shoulder, 'error_code': 'good'}

        # 4. Generic Evaluator for remaining exercises
        else:
            base_target = cfg['target_joint'].replace('left_', '').replace('right_', '')
            correct_min, correct_max = cfg['correct_range']
            
            for side in ['left', 'right']:
                joint_name = f"{side}_{base_target}"
                angle_val = angles.get(joint_name)
                
                if angle_val is not None:
                    if self.state == 'down':
                        is_correct = correct_min <= angle_val <= correct_max
                    else:
                        up = cfg['up_angle']
                        down = cfg['down_angle']
                        if down < up:
                            is_correct = angle_val >= (up - 25)
                        else:
                            is_correct = angle_val <= (up + 25)

                    if not is_correct:
                        ecode = "bend_more" if angle_val > correct_max else "extend_more"
                        status[joint_name] = {'correct': False, 'angle': angle_val, 'error_code': ecode}
                    else:
                        status[joint_name] = {'correct': True, 'angle': angle_val, 'error_code': 'good'}

        return status

    def update(self, angles):
        """Process angles and update rep counter. Returns feedback dict."""
        import time
        self.rep_complete = False
        self.frame_count += 1
        cfg = self.config

        # Autodetect highest engaged natural limb to avoid left/right mismatch
        base_target = cfg['target_joint'].replace('left_', '').replace('right_', '')
        left_angle = angles.get(f'left_{base_target}')
        right_angle = angles.get(f'right_{base_target}')
        
        down_thresh = cfg['down_angle']
        angle = None
        
        if left_angle is not None and right_angle is not None:
            if abs(left_angle - down_thresh) < abs(right_angle - down_thresh):
                angle = left_angle
            else:
                angle = right_angle
        elif left_angle is not None:
            angle = left_angle
        elif right_angle is not None:
            angle = right_angle

        if angle is None:
            return self._status('Detecting pose...', False)

        self.angle_history.append(angle)
        if len(self.angle_history) > 10:
            self.angle_history.pop(0)

        # Require minimum samples before evaluating
        if self.frame_count < self.min_samples:
            return self._status('Calibrating...', True)

        # Smoothed angle (last 5 frames)
        window = self.angle_history[-5:]
        smooth = sum(window) / len(window)

        down_thresh = cfg['down_angle']
        up_thresh = cfg['up_angle']
        correct_min, correct_max = cfg['correct_range']

        # Handle normal rep-based exercises
        if down_thresh < up_thresh:
            # Standard pattern (e.g., squat: down=90, up=160)
            if self.state == 'up':
                if smooth < down_thresh + 15:
                    self.state = 'down'
                    self.current_rep_correct = True
                    self.peak_angle = smooth
                    return self._status(cfg['feedback_down'], True)
                else:
                    self.posture_ok = True
                    return self._status('Ready — start the exercise', True)

            elif self.state == 'down':
                if smooth < (self.peak_angle or smooth):
                    self.peak_angle = smooth

                if smooth > up_thresh - 10:
                    self.state = 'up'
                    now = time.time()
                    if now - self.last_rep_time > 1.0:
                        self.last_rep_time = now
                        self.total_reps += 1
                        self.rep_complete = True

                        peak = self.peak_angle or smooth
                        if correct_min <= peak <= correct_max:
                            self.current_rep_correct = True
                        else:
                            self.current_rep_correct = False

                        if self.current_rep_correct:
                            self.correct_reps += 1
                            msg = cfg['feedback_correct']
                            ok = True
                        else:
                            msg = cfg['feedback_too_shallow']
                            ok = False

                        self.posture_ok = ok
                        return self._status(msg, ok, rep_done=True)
                    else:
                        self.posture_ok = True
                        return self._status('Too fast', True)

                self.posture_ok = True
                return self._status(cfg['feedback_up'], True)

        else:
            # Inverted pattern (e.g., bicep curl: down=160, up=40)
            if self.state == 'up':
                if smooth > down_thresh - 15:
                    self.state = 'down'
                    self.current_rep_correct = True
                    self.peak_angle = smooth
                    return self._status(cfg['feedback_down'], True)
                else:
                    self.posture_ok = True
                    return self._status('Ready — start the exercise', True)

            elif self.state == 'down':
                if smooth > (self.peak_angle or smooth):
                    self.peak_angle = smooth

                if smooth < up_thresh + 10:
                    self.state = 'up'
                    now = time.time()
                    if now - self.last_rep_time > 1.0:
                        self.last_rep_time = now
                        self.total_reps += 1
                        self.rep_complete = True

                        peak = self.peak_angle or smooth
                        if correct_min <= peak <= correct_max:
                            self.current_rep_correct = True
                        else:
                            self.current_rep_correct = False

                        if self.current_rep_correct:
                            self.correct_reps += 1
                            msg = cfg['feedback_correct']
                            ok = True
                        else:
                            msg = cfg['feedback_too_shallow']
                            ok = False

                        self.posture_ok = ok
                        return self._status(msg, ok, rep_done=True)
                    else:
                        self.posture_ok = True
                        return self._status('Too fast', True)

                self.posture_ok = True
                return self._status(cfg['feedback_up'], True)

        return self._status('', True)

    def posture_changed(self):
        """Check if posture state changed since last call (for audio triggers)."""
        changed = self.posture_ok != self._last_posture_state
        self._last_posture_state = self.posture_ok
        return changed

    def _status(self, msg, posture_ok, rep_done=False):
        self.posture_ok = posture_ok
        accuracy = (self.correct_reps / self.total_reps * 100) if self.total_reps > 0 else 0
        return {
            'feedback': msg,
            'posture_ok': posture_ok,
            'total_reps': self.total_reps,
            'correct_reps': self.correct_reps,
            'accuracy': round(accuracy, 1),
            'rep_complete': rep_done,
            'state': self.state,
            'peak_angle': self.peak_angle,
        }

    def get_summary(self):
        accuracy = (self.correct_reps / self.total_reps * 100) if self.total_reps > 0 else 0
        return {
            'exercise': self.config['name'],
            'total_reps': self.total_reps,
            'correct_reps': self.correct_reps,
            'accuracy': round(accuracy, 1),
        }

