import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langgraph.graph import StateGraph, END
from state.interview_state import InterviewState
from nodes.jd_node import parse_job_description
from nodes.interviewer_tone import set_interviewer_tone
from nodes.interviewer_node import interview_turn_node
from nodes.summarize_feedback_node import summarize_feedback_node

# Define LangGraph StateGraph
builder = StateGraph(InterviewState)

# Register Nodes
builder.add_node("parse_jd", parse_job_description)
builder.add_node("set_tone", set_interviewer_tone)
builder.add_node("interview_turn", interview_turn_node)
builder.add_node("summarize_feedback", summarize_feedback_node)

# Edges
builder.set_entry_point("parse_jd")
builder.add_edge("parse_jd", "set_tone")
builder.add_edge("set_tone", "interview_turn")

# Loop edge
def should_continue(state: InterviewState) -> str:
    max_turns = 5
    if state.get("turns", 0) >= max_turns:
        return "summarize_feedback"
    return "interview_turn"

builder.add_conditional_edges("interview_turn", should_continue)

# End
builder.add_edge("summarize_feedback", END)

# Compile graph
interview_graph = builder.compile()
