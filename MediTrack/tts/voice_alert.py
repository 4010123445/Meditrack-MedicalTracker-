import threading
import pyttsx3


def _speak_worker(message: str):
    try:
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()
    except Exception:
        pass


def speak_async(message: str):
    t = threading.Thread(target=_speak_worker, args=(message,), daemon=True)
    t.start()
