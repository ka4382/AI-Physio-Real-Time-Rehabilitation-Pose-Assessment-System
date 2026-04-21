from .base_exercise import BaseExercise

class DynamicExercise(BaseExercise):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.target_joint = config.get('target_joint', 'left_knee')
        self.down_angle = config.get('down_angle', 90)
        self.up_angle = config.get('up_angle', 160)
        
    def process(self, angles, landmarks=None):
        angle = angles.get(self.target_joint)
        if not angle:
            return self.get_state(), False
        
        rep_complete = False
        up_threshold = self.up_angle
        down_threshold = self.down_angle
        
        # Handle motion logic generically
        if self.down_angle < self.up_angle:
            # e.g., Squat (down is ~90, up is ~160)
            if angle > up_threshold - 15:
                if self.stage == 'down':
                    self.counter += 1
                    rep_complete = True
                    self.feedback = self.config.get('feedback_correct', "Perfect rep!")
                self.stage = 'up'
            elif angle < down_threshold + 15:
                if self.stage == 'up':
                    self.feedback = self.config.get('feedback_down', "Good depth.")
                self.stage = 'down'
        else:
            # e.g., Bicep curl (down is ~160, up is ~40)
            if angle < up_threshold + 15:
                if self.stage == 'down':
                    self.counter += 1
                    rep_complete = True
                    self.feedback = self.config.get('feedback_correct', "Perfect rep!")
                self.stage = 'up'
            elif angle > down_threshold - 15:
                if self.stage == 'up':
                    self.feedback = self.config.get('feedback_down', "Full extension.")
                self.stage = 'down'
                
        self.posture_ok = True
        state = self.get_state()
        state['rep_complete'] = rep_complete
        state['peak_angle'] = angle
        return state, True
