from typing import List

from pydantic import BaseModel, Field


class AnalysisModel(BaseModel):
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    summary: str = ""
    hiring_recommendation: str = ""
    interview_focus: List[str] = Field(default_factory=list)
