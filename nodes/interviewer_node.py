# interview_turn_node.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import threading
import time
from utils.webcam_emotion import start_emotion_stream
from utils.audio_transcriber import record_and_transcribe
from utils.gpt_question_generator import generate_interview_question
from utils.text_to_speech import speak_text
from state.interview_state import InterviewState


def interview_turn_node(state: InterviewState) -> InterviewState:
    """
    Runs a single turn of the interview:
    1. Generates a GPT-based question
    2. Speaks the question aloud (TTS)
    3. Starts live webcam emotion detection (in background thread)
    4. Records user's audio + transcribes it
    5. Logs question, answer, emotion
    6. Updates state
    """
    # 1. Generate GPT Question
    question = generate_interview_question(
        jd=state["job_description"],
        tone=state["interviewer_tone"],
        history=state.get("qa_history", [])
    )
    state["current_question"] = question
    print(f"\n🧠 Interview Question:\n{question}\n")

    # 2. Speak question aloud (TTS)
    speak_text(question)

    # 3. Start Emotion Stream (async)
    emotion_log = []
    stop_flag = threading.Event()

    emotion_thread = threading.Thread(
        target=start_emotion_stream,
        args=(emotion_log, stop_flag)
    )
    emotion_thread.start()

    # 4. Start Audio Recording + Transcription
    print("🎤 Please answer. Recording started...\n")
    answer_text = record_and_transcribe(timeout=30)  # 30s max per answer

    # 5. Stop Emotion Stream
    stop_flag.set()
    emotion_thread.join()

    # 6. Get dominant emotion during answer
    dominant_emotion = emotion_log[-1] if emotion_log else "neutral"

    # 7. Log Q/A + Emotion to state
    state.setdefault("qa_history", []).append((question, answer_text))
    state.setdefault("emotion_log", []).append(dominant_emotion)
    state["turns"] = state.get("turns", 0) + 1

    print(f"✅ Transcription:\n{answer_text}")
    print(f"😊 Detected Emotion: {dominant_emotion}\n")

    return state
