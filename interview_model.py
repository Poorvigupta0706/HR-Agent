from typing import List

from pydantic import BaseModel, Field


class InterviewSection(BaseModel):
    title: str = ""
    questions: List[str] = Field(default_factory=list)


class InterviewQuestionsModel(BaseModel):
    sections: List[InterviewSection] = Field(default_factory=list)
