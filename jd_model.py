from pydantic import BaseModel, Field, field_validator
from typing import List


class JDModel(BaseModel):
    skills: List[str] = Field(default_factory=list)
    experience: List[str] = Field(default_factory=list)
    qualifications: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)

    @field_validator(
        "skills",
        "experience",
        "qualifications",
        "certifications",
        mode="before",
    )
    @classmethod
    def empty_string_to_list(cls, v):
        if v == "" or v is None:
            return []
        return v