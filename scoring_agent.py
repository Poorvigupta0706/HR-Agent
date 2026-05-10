import numpy as np
from config import llm
from score_model import ScoreModel
structured_llm = llm.with_structured_output(ScoreModel)
def embedding_similarity(jd_emb, resume_emb):
    similarity = np.dot(jd_emb, resume_emb) / (
        np.linalg.norm(jd_emb) *
        np.linalg.norm(resume_emb)
    )

    return round(float(similarity) * 100, 2)
def scoring_agent(jd,
                  resume,
                  jd_emb,
                  resume_emb):

    semantic_score = embedding_similarity(
        jd_emb,
        resume_emb
    )

    prompt = f"""
    You are an ATS scoring engine.

    Evaluate candidate using this rubric:

    Skills Match: 35%
    Experience Match: 25%
    Projects/Relevance: 15%
    Education: 10%
    Certifications: 5%
    Semantic Similarity: 10%

    JOB DESCRIPTION:
    {jd}

    CANDIDATE RESUME:
    {resume}

    SEMANTIC SIMILARITY SCORE:
    {semantic_score}

    Return:
    - skills_score
    - experience_score
    - project_score
    - education_score
    - certification_score
    - semantic_score
    - total_score
    - recommendation
    - strengths
    - weaknesses
    - confidence_level

    Rules:
    - Scores must be between 0 and 10
    - total_score should be out of 100
    - recommendation should be:
      Hire / Maybe / Reject
    """

    response = structured_llm.invoke(prompt)

    return response