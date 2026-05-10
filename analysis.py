from analysis_model import AnalysisModel
from config import llm

structured_llm = llm.with_structured_output(AnalysisModel, method="json_mode")


def analysis_agent(jd, resume, score):
    prompt = f"""
    You are an HR recruiter analyzing a candidate for a role.
    You must return the response in JSON format.

    Return:
    - strengths
    - weaknesses
    - missing_skills
    - summary
    - hiring_recommendation
    - interview_focus

    Rules:
    - The summary should be 2 to 4 sentences.
    - Keep lists concise and specific to the candidate.
    - Base the response on the JD, resume, and ATS score.

    JD:
    {jd}

    Resume:
    {resume}

    Score:
    {score}
    """
    return structured_llm.invoke(prompt)
