# utils/gpt_question_generator.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()
# Load OpenAI model
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)

# Prompt Template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", 
     "You are acting as a job interviewer. Ask one question at a time. "
     "Your tone should be {interviewer_tone}. Use the job description to keep questions relevant."),
    
    ("user",
     "Job Description:\n{job_description}\n\n"
     "Previous Q/A:\n{qa_history}\n\n"
     "Now, ask the next best question.")
])


def generate_interview_question(jd: str, tone: str, history: list[tuple[str, str]]) -> str:
    """
    Generate a contextual interview question based on:
    - job description (jd)
    - interviewer_tone (e.g., 'Formal', 'Friendly')
    - qa_history: list of (question, answer) tuples

    Returns: GPT-generated question string.
    """
    history_str = "\n".join([f"Q: {q}\nA: {a}" for q, a in history[-5:]])  # last 5 Q/A max

    chain = prompt_template | llm
    response = chain.invoke({
        "job_description": jd,
        "interviewer_tone": tone,
        "qa_history": history_str
    })

    return str(response.content).strip()
