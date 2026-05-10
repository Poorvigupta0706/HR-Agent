from config import llm
from interview_model import InterviewQuestionsModel

structured_llm = llm.with_structured_output(InterviewQuestionsModel, method="json_mode")


def interview_agent(jd, resume):
    prompt = f"""
    Generate grouped interview questions for this candidate.
    You must return the response in JSON format.

    Return 4 to 6 sections, and each section should include:
    - title
    - questions

    Rules:
    - Each section should have 2 to 4 questions.
    - Keep questions practical and interview-ready.
    - Cover background, technical depth, projects, role fit, and behavior.

    JD:
    {jd}

    Resume:
    {resume}
    """
    return structured_llm.invoke(prompt)
