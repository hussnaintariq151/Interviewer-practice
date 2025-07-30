# nodes/summarize_feedback_node.py

from state.interview_state import InterviewState
from openai import OpenAI

client = OpenAI()

def summarize_feedback_node(state: InterviewState) -> InterviewState:
    """
    Analyzes the interview Q&A and emotions to generate feedback summary.
    Updates:
        - state["feedback_summary"]
        - state["score"]
    """
    qa_history = state.get("qa_history", [])
    emotion_log = state.get("emotion_log", [])
    tone = state.get("interviewer_tone", "Formal")
    jd = state.get("job_description", "")

    if not qa_history:
        state["feedback_summary"] = "No interview responses found to analyze."
        state["score"] = 0
        return state

    # Format QA for GPT
    qa_pairs = "\n\n".join(
        [f"Q{i+1}: {q}\nA{i+1}: {a}" for i, (q, a) in enumerate(qa_history)]
    )
    emotions = ", ".join(emotion_log)

    prompt = f"""
You are an AI interview coach.

Here is the job description:
{jd}

The interviewer tone was: {tone}

Here is the full interview log:
{qa_pairs}

The candidate's observed emotions during the responses: {emotions}

Based on the above:
1. Provide an overall evaluation of the candidate's performance.
2. Highlight their strengths and weaknesses.
3. Assign a score out of 10.
4. Give 3 specific suggestions to improve.

Respond in a professional tone.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    summary = response.choices[0].message.content.strip()

    state["feedback_summary"] = summary

    # Extract score from summary (fallback = 7.0)
    import re
    match = re.search(r"score.*?(\d(?:\.\d)?)/?10", summary, re.IGNORECASE)
    state["score"] = float(match.group(1)) if match else 7.0

    return state
