
from state.interview_state import InterviewState

def parse_job_description(state: InterviewState) -> InterviewState:
    """
    Stores the job description in InterviewState.
    Assumes the full JD text is already provided by the user.
    """
    jd_text = state.get("job_description", "")
    if not jd_text or len(jd_text.strip()) < 20:
        raise ValueError("Invalid or too short job description.")
    
    state["job_description"] = jd_text.strip()
    return state
