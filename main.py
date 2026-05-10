import os
from dotenv import load_dotenv
load_dotenv()
print(
    "LangSmith Project:",
    os.getenv("LANGCHAIN_PROJECT")
)
from resume import extract_resume_text
from jd_agent import jd_agent
from resume_agent import resume_agent
from embeddings_agent import embedding_agent
from scoring_agent import scoring_agent
jd_text = extract_resume_text(r"C:\Users\dell\PycharmProjects\HR-Agent\dataset\Daksh_Jain_FlowCV_Resume_2026-04-11 (2) (1).pdf")
resume_text = extract_resume_text(
    r"C:\Users\dell\PycharmProjects\HR-Agent\dataset\Daksh_Jain_FlowCV_Resume_2026-04-11 (2) (1).pdf"
)
jd = jd_agent(jd_text)
print("\n===== JD ANALYSIS =====\n")
print(jd)
resume = resume_agent(resume_text)
print("\n===== RESUME ANALYSIS =====\n")
print(resume)
jd_emb = embedding_agent(str(jd))
resume_emb = embedding_agent(
    str(resume)
)
score = scoring_agent(
    jd,
    resume,
    jd_emb,
    resume_emb
)
print("\n===== ATS SCORE =====\n")
print(score)