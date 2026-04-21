from .base_exercise import BaseExercise
import math

class NeckExercise(BaseExercise):
    def process(self, angles, landmarks=None):
        # Graceful fallback metric since neck tilt isn't physically tracked by standard angles map yet
        tilt = angles.get('neck_tilt', 0)
        
        rep_complete = False
        if self.stage != 'active':
            self.stage = 'active'
            self.feedback = "Tilt your head gently."
            
        state = self.get_state()
        state['rep_complete'] = rep_complete
        state['peak_angle'] = tilt
        return state, True
