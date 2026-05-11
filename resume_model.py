from pydantic import BaseModel
from typing import List
class ResumeModel(BaseModel):
    name: str
    skills: List[str]
    experience: List[str]
    education: List[str]
    projects: List[str]
    certifications: List[str]
    strengths: List[str]
    weaknesses: List[str]