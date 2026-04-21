from .base_exercise import BaseExercise

class BicepExercise(BaseExercise):
    def process(self, angles, landmarks=None):
        angle = angles.get('right_elbow') or angles.get('left_elbow')
        if not angle:
            return self.get_state(), False
        
        rep_complete = False
        if angle > 150:
            if self.stage == 'up':
                self.counter += 1
                rep_complete = True
                self.feedback = "Full extension."
            self.stage = 'down'
        elif angle < 45:
            if self.stage == 'down':
                self.feedback = "Squeeze at the top."
            self.stage = 'up'
            
        state = self.get_state()
        state['rep_complete'] = rep_complete
        state['peak_angle'] = angle
        return state, True
