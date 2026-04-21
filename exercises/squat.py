from .base_exercise import BaseExercise

class SquatExercise(BaseExercise):
    def process(self, angles, landmarks=None):
        angle = angles.get('left_knee') or angles.get('right_knee')
        if not angle:
            return self.get_state(), False
        
        rep_complete = False
        if angle > 160:
            if self.stage == 'down':
                self.counter += 1
                rep_complete = True
                self.feedback = "Perfect squat! Stand up fully."
            self.stage = 'up'
        elif angle < 90:
            if self.stage == 'up':
                self.feedback = "Great depth. Push up."
            self.stage = 'down'
            
        self.posture_ok = True
        state = self.get_state()
        state['rep_complete'] = rep_complete
        state['peak_angle'] = angle
        return state, True
