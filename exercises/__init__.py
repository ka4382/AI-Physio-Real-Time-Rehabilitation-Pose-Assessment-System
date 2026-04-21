from .squat import SquatExercise
from .arm_raise import ArmRaiseExercise
from .bicep import BicepExercise
from .neck import NeckExercise
from .dynamic import DynamicExercise
from services.exercise_service import EXERCISES

def get_exercise_handler(name):
    # Map the raw string sent by UI to the handler class
    handlers = {
        'squat': SquatExercise,
        'arm_raise': ArmRaiseExercise,
        'bicep_curl': BicepExercise,
        'neck_stretch': NeckExercise
    }
    n = name.lower() if name else 'squat'
    if n in handlers:
        return handlers[n]()
    
    # Fallback to configuration-based dynamic processing for all other generic exercises
    config = EXERCISES.get(n)
    if config:
        return DynamicExercise(config)
        
    return SquatExercise()
