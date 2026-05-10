from config import llm
from jd_model import JDModel

structured_llm = llm.with_structured_output(JDModel)


def jd_agent(jd_text):

    prompt = f"""
    Extract:

    - Skills
    - Experience
    - Qualifications

    JD:
    {jd_text}
    """

    return structured_llm.invoke(prompt)