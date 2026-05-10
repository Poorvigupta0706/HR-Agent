from typing import List, Any

from pydantic import BaseModel, Field


class ResumeModel(BaseModel):
    name: str = ""
    skills: List[str] = Field(default_factory=list)
    experience: List[Any] = Field(default_factory=list)
    education: List[Any] = Field(default_factory=list)
    projects: List[Any] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
