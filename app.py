import streamlit as st
import fitz
import docx
import uuid

from jd_agent import jd_agent
from resume_agent import resume_agent
from embeddings_agent import embedding_agent
from scoring_agent import scoring_agent
from analysis import analysis_agent
from interview import interview_agent
from override import log_override

st.set_page_config(page_title="AI HR ATS System", layout="wide")
st.title("AI HR ATS System")


# ---------------------------
# RESUME TEXT EXTRACTION
# ---------------------------
def extract_resume_text(file, file_type):
    text = ""
    if file_type == "pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()

    elif file_type == "docx":
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text


# ---------------------------
# INPUTS
# ---------------------------
jd_text = st.text_area("Paste Job Description")
uploaded_resume = st.file_uploader("Upload Resume", type=["pdf", "docx"])


# ---------------------------
# SESSION STATE INIT
# ---------------------------
if "candidate_id" not in st.session_state:
    st.session_state.candidate_id = str(uuid.uuid4())

if "result" not in st.session_state:
    st.session_state.result = None

if "final_score" not in st.session_state:
    st.session_state.final_score = None


# ---------------------------
# ANALYZE BUTTON
# ---------------------------
if st.button("Analyze Candidate"):

    if uploaded_resume and jd_text:

        file_type = uploaded_resume.name.split(".")[-1]
        resume_text = extract_resume_text(uploaded_resume, file_type)

        jd = jd_agent(jd_text)
        resume = resume_agent(resume_text)

        jd_emb = embedding_agent(str(jd))
        resume_emb = embedding_agent(str(resume))

        score = scoring_agent(jd, resume, jd_emb, resume_emb)
        analysis = analysis_agent(jd, resume, score)
        questions = interview_agent(jd, resume)

        # SAVE FULL RESULT (IMPORTANT)
        st.session_state.result = {
            "score": score,
            "analysis": analysis,
            "questions": questions
        }

        # default final score = AI score
        st.session_state.final_score = float(score.total_score)

    else:
        st.warning("Please upload resume and paste JD")


# ---------------------------
# DISPLAY RESULTS
# ---------------------------
if st.session_state.result:

    st.subheader("AI Generated Score")
    st.write(st.session_state.result["score"])

    st.subheader("Candidate Analysis")
    st.write(st.session_state.result["analysis"])

    st.subheader("Interview Questions")
    st.write(st.session_state.result["questions"])


    # ---------------------------
    # HR OVERRIDE PANEL
    # ---------------------------
    st.subheader("HR Override Panel")

    new_score = st.number_input(
        "Adjust Score",
        min_value=0.0,
        max_value=100.0,
        value=float(st.session_state.final_score),
        step=1.0
    )

    reason = st.text_area("Reason for override (mandatory)")


    if st.button("Save Override"):

        if reason.strip() == "":
            st.error("Reason is required for override")

        else:
            log_override(
                candidate_id=st.session_state.candidate_id,
                old_score=st.session_state.final_score,
                new_score=new_score,
                reason=reason
            )

            st.session_state.final_score = new_score
            st.success("Override saved successfully!")


    # ---------------------------
    # FINAL SCORE
    # ---------------------------
    st.subheader("Final Score (After HR Review)")
    st.metric("Score", st.session_state.final_score)

else:
    st.info("Upload resume and click Analyze Candidate") 