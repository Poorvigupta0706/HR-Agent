from config import llm
def interview_agent(jd, resume):
    prompt = f"""
    Generate interview questions.
    JD:
    {jd}
    Resume:
    {resume}
    """
    return llm.invoke(prompt).content