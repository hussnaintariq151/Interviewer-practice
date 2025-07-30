# utils/audio_transcriber.py

import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import os
from faster_whisper import WhisperModel


# Load model globally to avoid reloading every time
model = WhisperModel("base", device="cpu", compute_type="int8")

def record_and_transcribe(timeout=30) -> str:
    """
    Records audio for up to `timeout` seconds and transcribes using FasterWhisper.
    Returns the transcribed text.
    """
    print(f"🎙️ Recording for {timeout} seconds... Speak now.")
    
    fs = 16000  # Sampling rate
    duration = timeout

    # Record audio from mic
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished

    # Save to temporary .wav file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        write(tmpfile.name, fs, audio)
        temp_path = tmpfile.name

    # Transcribe
    print("🔍 Transcribing with FasterWhisper...")
    segments, _ = model.transcribe(temp_path)
    transcription = " ".join([seg.text for seg in segments])

    # Clean up temp file
    os.remove(temp_path)

    return transcription.strip()
