import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ai-physio-secret-2024')
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'physio.db')
    CAMERA_INDEX = 0
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    FPS_TARGET = 30
    MIN_DETECTION_CONFIDENCE = 0.7
    MIN_TRACKING_CONFIDENCE = 0.7
    AUDIO_ENABLED = True
    AUDIO_COOLDOWN = 2  # seconds between audio cues
