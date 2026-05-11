import os
from jd_model import JDModel
from resume_model import ResumeModel
from scoring_agent import scoring_agent
import numpy as np

# Mock JD
jd = JDModel(
    skills=["UI/UX", "Frontend Development", "API Integration"],
    experience=["3 years"],
    qualifications=["Bachelors"],
    certifications=["AWS"]
)

# Mock Resume
resume = ResumeModel(
    name="John Doe",
    skills=["UI/UX", "Frontend Development", "React"],
    experience=["Frontend Dev at ABC"],
    education=["Bachelors in CS"],
    projects=[],
    certifications=[],
    strengths=[],
    weaknesses=[]
)

jd_emb = np.random.rand(768)
resume_emb = np.random.rand(768)

score = scoring_agent(jd, resume, jd_emb, resume_emb)
print(f"JD Match Score: {score.jd_match_score}")
