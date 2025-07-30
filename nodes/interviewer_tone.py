

from state.interview_state import InterviewState

VALID_TONES = ["Formal", "Friendly", "Assertive", "Casual"]

def set_interviewer_tone(state: InterviewState) -> InterviewState:
    """
    Sets and validates the interviewer tone based on user selection.
    Updates `interviewer_tone` in InterviewState.
    """
    tone = state.get("interviewer_tone", "").capitalize()

    if tone not in VALID_TONES:
        raise ValueError(f"Invalid interviewer tone '{tone}'. Choose from: {VALID_TONES}")

    state["interviewer_tone"] = tone
    return state
