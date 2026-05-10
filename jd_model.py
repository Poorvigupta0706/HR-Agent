from pydantic import BaseModel
from typing import List
class JDModel(BaseModel):
    skills: List[str]
    experience: str
    qualifications: List[str]
    certifications: List[str]