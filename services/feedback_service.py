import threading
import time
import logging

logger = logging.getLogger(__name__)

try:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    logger.warning("pyttsx3 not available — audio feedback disabled")

last_spoken = 0

def speak(text):
    global last_spoken
    if not TTS_AVAILABLE:
        return
        
    if time.time() - last_spoken > 3:
        try:
            # We track time before triggering to strictly bounce parallel threads
            last_spoken = time.time()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            logger.error(f"[Audio] Speak error: {e}")

class FeedbackService:
    def __init__(self, audio_enabled=True, cooldown=3):
        self.audio_enabled = audio_enabled and TTS_AVAILABLE
        self.cooldown = cooldown
        self._last_posture_ok = True

    def speak(self, message, priority=False):
        """Safely trigger TTS inside a detached thread."""
        if not self.audio_enabled:
            return
        threading.Thread(target=speak, args=(message,), daemon=True).start()

    def give_feedback(self, feedback_msg, posture_ok, rep_complete=False, posture_changed=False):
        if not feedback_msg:
            return

        # Trigger audio ONLY when needed, relying on 3s cooldown to prevent overlap
        if rep_complete:
            self.speak(feedback_msg, priority=True)
        elif not posture_ok:
            self.speak(feedback_msg)
        elif posture_changed and posture_ok:
            self.speak("Good form")

        # Update tracked state
        self._last_posture_ok = posture_ok
