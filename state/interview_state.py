# state/interview_state.py

from typing import TypedDict, List, Optional, Tuple

class InterviewState(TypedDict, total=False):
    # 🟩 Static Inputs
    job_description: Optional[str]             # Raw JD text from user
    interviewer_tone: Optional[str]            # Selected from dropdown (Formal, Friendly, etc.)

    # 🔁 Dynamic Interview Loop
    current_question: Optional[str]            # Most recent GPT-generated question
    qa_history: List[Tuple[str, str]]          # List of (question, answer) tuples
    emotion_log: List[str]                     # List of dominant emotions per turn

    # 🧠 Internal Tracking
    turns: int                                 # Number of completed Q&A rounds

    # 📊 Final Feedback
    feedback_score: Optional[float]            # Scored at the end (optional)
    feedback_summary: Optional[str]            # LLM-generated feedback (optional)
