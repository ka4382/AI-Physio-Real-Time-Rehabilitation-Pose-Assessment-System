from .base_exercise import BaseExercise

class ArmRaiseExercise(BaseExercise):
    def process(self, angles, landmarks=None):
        angle = angles.get('right_shoulder') or angles.get('left_shoulder')
        if not angle:
            return self.get_state(), False
        
        rep_complete = False
        if angle < 30:
            if self.stage == 'up':
                self.counter += 1
                rep_complete = True
                self.feedback = "Good tempo."
            self.stage = 'down'
        elif angle > 150:
            if self.stage == 'down':
                self.feedback = "Raise higher."
            self.stage = 'up'
            
        state = self.get_state()
        state['rep_complete'] = rep_complete
        state['peak_angle'] = angle
        return state, True
