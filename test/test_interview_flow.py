
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from graph.langgraph_flow import interview_graph
from state.interview_state import InterviewState

# 🎯 Fill in realistic values
initial_state: InterviewState = {
    "job_description": "We are hiring an AI engineer to build deep learning systems using PyTorch and deploy them using Docker + FastAPI.",
    "interviewer_tone": "Friendly",
    "turns": 0,
    "qa_history": [],
    "emotion_log": []
}

# 🚀 Run the graph
final_state = interview_graph.invoke(initial_state)

# 📊 Output final feedback
print("\n✅ Interview Completed.")
print("\n📋 Feedback Summary:\n", final_state.get("feedback_summary", "No summary available."))
print("\n📈 Score:", final_state.get("score", "N/A"))
