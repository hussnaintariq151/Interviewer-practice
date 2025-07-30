# utils/text_to_speech.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pyttsx3

def speak_text(text: str):
    """Speak text aloud using pyttsx3."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)  # Speech speed
    engine.say(text)
    engine.runAndWait()
