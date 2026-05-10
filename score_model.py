from pydantic import BaseModel
from typing import List


class ScoreModel(BaseModel):

    skills_score: int

    experience_score: int

    project_score: int

    education_score: int

    certification_score: int

    semantic_score: float

    total_score: float

    recommendation: str

    strengths: List[str]

    weaknesses: List[str]

    confidence_level: str