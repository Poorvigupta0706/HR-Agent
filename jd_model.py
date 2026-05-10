from typing import List

from pydantic import BaseModel, Field


class JDModel(BaseModel):
    skills: List[str] = Field(default_factory=list)
    experience: List[str] = Field(default_factory=list)
    qualifications: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
