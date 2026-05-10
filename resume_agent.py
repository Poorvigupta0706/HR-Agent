from config import llm
from resume_model import ResumeModel

structured_llm = llm.with_structured_output(ResumeModel, method="json_mode")


def resume_agent(resume_text):
    prompt = f"""
    Analyze the candidate resume and extract structured information.
    You must return the response in JSON format.

    Return:
    - name
    - skills
    - experience
    - education
    - projects
    - certifications
    - strengths
    - weaknesses

    Rules:
    - Use short, clean phrases.
    - Keep lists concise and relevant.
    - If a field is missing, return an empty string or empty list.

    Resume:
    {resume_text}
    """

    return structured_llm.invoke(prompt)
