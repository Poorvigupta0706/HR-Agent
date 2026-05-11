import numpy as np

from config import llm
from score_model import ScoreModel

structured_llm = llm.with_structured_output(ScoreModel, method="json_mode")


def embedding_similarity(jd_emb, resume_emb):
    similarity = np.dot(jd_emb, resume_emb) / (
        np.linalg.norm(jd_emb) * np.linalg.norm(resume_emb)
    )
    return round(float(similarity) * 100, 2)


def jd_match_score(jd_skills, resume_skills):
    if not jd_skills:
        return 0

    match_count = 0
    for j_skill in jd_skills:
        j_lower = j_skill.lower()
        # Check if the JD skill is a substring of any resume skill, or vice versa
        if any(j_lower in r.lower() or r.lower() in j_lower for r in resume_skills):
            match_count += 1
            
    match = match_count / len(jd_skills)
    return round(match * 100, 2)


def normalize_ten_point_score(value):
    return round(max(0.0, min(10.0, float(value))), 1)


def semantic_score_to_ten_point_scale(similarity_score):
    return normalize_ten_point_score(similarity_score / 10)


def total_score_from_components(score):
    return round(
        (score.skills_score * 3.5)
        + (score.experience_score * 2.5)
        + (score.project_score * 1.5)
        + (score.education_score * 1.0)
        + (score.certification_score * 0.5)
        + (score.semantic_score * 1.0),
        1,
    )


def recommendation_from_total(total_score):
    if total_score >= 75:
        return "Hire"
    if total_score >= 55:
        return "Maybe"
    return "Reject"


def confidence_from_scores(total_score, jd_match):
    if total_score >= 75 and jd_match >= 65:
        return "High"
    if total_score >= 55:
        return "Medium"
    return "Low"


def scoring_agent(jd, resume, jd_emb, resume_emb):
    semantic_similarity = embedding_similarity(jd_emb, resume_emb)

    jd_skills = jd.get("skills", []) if isinstance(jd, dict) else getattr(jd, "skills", [])
    resume_skills = resume.get("skills", []) if isinstance(resume, dict) else getattr(resume, "skills", [])
    jd_match = jd_match_score(jd_skills, resume_skills)

    prompt = f"""
    You are an ATS scoring engine.
    You must return the response in JSON format.

    Evaluate the candidate with these weighted categories:
    - skills_score
    - experience_score
    - project_score
    - education_score
    - certification_score

    Additional context:
    - semantic similarity percentage: {semantic_similarity}
    - JD skill match percentage: {jd_match}

    JOB DESCRIPTION:
    {jd}

    CANDIDATE RESUME:
    {resume}

    Return:
    - skills_score
    - experience_score
    - project_score
    - education_score
    - certification_score
    - semantic_score
    - strengths
    - weaknesses

    Rules:
    - All scores must be between 0 and 10.
    - strengths and weaknesses should be short phrases.
    - semantic_score should reflect the overall relevance on a 0 to 10 scale.
    """

    response = structured_llm.invoke(prompt)

    response.skills_score = normalize_ten_point_score(response.skills_score)
    response.experience_score = normalize_ten_point_score(response.experience_score)
    response.project_score = normalize_ten_point_score(response.project_score)
    response.education_score = normalize_ten_point_score(response.education_score)
    response.certification_score = normalize_ten_point_score(response.certification_score)
    response.semantic_score = semantic_score_to_ten_point_scale(semantic_similarity)
    response.total_score = total_score_from_components(response)
    response.recommendation = recommendation_from_total(response.total_score)
    response.confidence_level = confidence_from_scores(response.total_score, jd_match)
    response.jd_match_score = jd_match

    return response
