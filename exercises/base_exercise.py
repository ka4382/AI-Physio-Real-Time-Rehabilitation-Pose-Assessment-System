class BaseExercise:
    def __init__(self):
        self.counter = 0
        self.correct_reps = 0
        self.stage = None
        self.posture_ok = True
        self.feedback = "Get into position"

    def process(self, angles, landmarks=None):
        """Processes the frame payload and returns (state_dict, pose_detected)"""
        raise NotImplementedError()

    def get_state(self):
        return {
            'total_reps': self.counter,
            'posture_ok': self.posture_ok,
            'feedback': self.feedback,
            'stage': self.stage
        }
    
    def reset(self):
        self.counter = 0
        self.correct_reps = 0
        self.stage = None
        self.posture_ok = True
        self.feedback = "Get into position"
        
    def get_summary(self):
        acc = (self.correct_reps / self.counter * 100) if self.counter > 0 else 0
        return {
            'total_reps': self.counter,
            'accuracy': int(acc)
        }
