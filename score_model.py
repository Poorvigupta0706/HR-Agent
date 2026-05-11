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
    jd_match_score: float
class ExplainableAI:

    @staticmethod
    def generate_strengths(data: dict) -> List[str]:
        strengths = []

        if data["skills_score"] >= 80:
            strengths.append("Strong technical skillset")

        if data["experience_score"] >= 75:
            strengths.append("Relevant industry experience")

        if data["project_score"] >= 80:
            strengths.append("Impressive project portfolio")

        if data["semantic_score"] >= 0.8:
            strengths.append("High job-role match based on resume semantics")

        if data["certification_score"] >= 70:
            strengths.append("Relevant certifications present")

        return strengths

    @staticmethod
    def generate_weaknesses(data: dict) -> List[str]:
        weaknesses = []

        if data["skills_score"] < 60:
            weaknesses.append("Weak technical skillset")

        if data["experience_score"] < 50:
            weaknesses.append("Insufficient work experience")

        if data["project_score"] < 60:
            weaknesses.append("Limited project exposure")

        if data["certification_score"] < 50:
            weaknesses.append("Lacks relevant certifications")

        if data["semantic_score"] < 0.6:
            weaknesses.append("Low role-match relevance")

        return weaknesses

    @staticmethod
    def generate_recommendation(total_score: float) -> str:
        if total_score >= 80:
            return "Strong Fit – Recommend for hiring"
        elif total_score >= 60:
            return "Moderate Fit – Consider for interview"
        else:
            return "Weak Fit – Not recommended"

    @staticmethod
    def generate_confidence(total_score: float) -> str:
        if total_score >= 80:
            return "High"
        elif total_score >= 60:
            return "Medium"
        else:
            return "Low"

    @staticmethod
    def create_score(data: dict) -> ScoreModel:

        total = (
            data["skills_score"] * 0.25 +
            data["experience_score"] * 0.25 +
            data["project_score"] * 0.20 +
            data["education_score"] * 0.10 +
            data["certification_score"] * 0.10 +
            data["semantic_score"] * 10  # scale semantic score
        )

        strengths = ExplainableAI.generate_strengths(data)
        weaknesses = ExplainableAI.generate_weaknesses(data)
        recommendation = ExplainableAI.generate_recommendation(total)
        confidence = ExplainableAI.generate_confidence(total)

        return ScoreModel(
            skills_score=data["skills_score"],
            experience_score=data["experience_score"],
            project_score=data["project_score"],
            education_score=data["education_score"],
            certification_score=data["certification_score"],
            semantic_score=data["semantic_score"],
            total_score=round(total, 2),
            recommendation=recommendation,
            strengths=strengths,
            weaknesses=weaknesses,
            confidence_level=confidence
        )