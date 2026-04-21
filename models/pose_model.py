# Extensible pose model wrapper
# Currently wraps MediaPipe BlazePose via PoseService
# Can be extended to swap in alternative backends (e.g., MoveNet, YOLO-pose)

class PoseModelConfig:
    MODEL_COMPLEXITY = 1  # 0=lite, 1=full, 2=heavy
    SMOOTH_LANDMARKS = True
    ENABLE_SEGMENTATION = False
    SMOOTH_SEGMENTATION = False
