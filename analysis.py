from config import llm
def analysis_agent(jd, resume, score):
    prompt = f"""
    You are an HR recruiter.

    Analyze this candidate.

    JD:
    {jd}
    Resume:
    {resume}
    Score:
    {score}
    Give:
    - strengths
    - weaknesses
    - missing skills
    - hiring recommendation
    """
    return llm.invoke(prompt).content