from typing import List

from pydantic import BaseModel, Field


class ScoreModel(BaseModel):
    skills_score: float = 0
    experience_score: float = 0
    project_score: float = 0
    education_score: float = 0
    certification_score: float = 0
    semantic_score: float = 0
    total_score: float = 0
    recommendation: str = ""
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    confidence_level: str = ""
    jd_match_score: float = 0
