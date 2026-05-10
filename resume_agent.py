from config import llm
from resume_model import ResumeModel

structured_llm = llm.with_structured_output(ResumeModel)
def resume_agent(resume_text):

    prompt = f"""
    Analyze candidate resume.

    Extract:
    - skills
    - experience
    - projects
    - strengths
    - weaknesses
    - certifications

    Resume:
    {resume_text}
    """

    return structured_llm.invoke(prompt)