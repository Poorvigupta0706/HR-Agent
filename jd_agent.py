from config import llm
from jd_model import JDModel

structured_llm = llm.with_structured_output(JDModel, method="json_mode")


def jd_agent(jd_text):
    prompt = f"""
    Extract structured hiring requirements from this job description.
    You must return the response in JSON format.

    Return:
    - skills
    - experience
    - qualifications
    - certifications

    Rules:
    - Use concise phrases.
    - If a field is not present, return an empty list [].

    JD:
    {jd_text}
    """

    return structured_llm.invoke(prompt)
