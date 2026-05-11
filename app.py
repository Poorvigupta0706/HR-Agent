import textwrap
import html
import uuid

import docx
import fitz
import streamlit as st

import re
def render_html(html_str):
    cleaned = re.sub(r'^[ \t]+', '', html_str, flags=re.MULTILINE)
    st.markdown(cleaned, unsafe_allow_html=True)


from analysis import analysis_agent
from embeddings_agent import embedding_agent
from interview import interview_agent
from jd_agent import jd_agent
from override_utils import log_override, validate_override
from resume_agent import resume_agent
from scoring_agent import scoring_agent

st.set_page_config(page_title="AI HR ATS System", layout="wide")

TABS = [
    "Job Description",
    "AI Score",
    "Analysis",
    "Questions",
    "HR Override",
]

SUBSCORE_META = [
    ("Skills", "skills_score", "#185FA5"),
    ("Experience", "experience_score", "#BA7517"),
    ("Projects", "project_score", "#185FA5"),
    ("Education", "education_score", "#3B6D11"),
    ("Certs", "certification_score", "#A32D2D"),
    ("Semantic", "semantic_score", "#0F6E56"),
]


def init_session_state():
    defaults = {
        "candidate_id": str(uuid.uuid4()),
        "nav_selection": TABS[0],
        "result": None,
        "final_score": None,
        "override_score": None,
        "override_reason_text": "",
        "override_feedback": "",
        "resume_file_name": "",
        "resume_file_size": 0,
        "jd_text_input": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def inject_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        @import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css');

        :root {
            --color-background-primary: #ffffff;
            --color-background-secondary: #fafafa;
            --color-background-tertiary: #f3f4f6;
            --color-background-info: #E6F1FB;
            --color-border-secondary: #e5e7eb;
            --color-border-tertiary: #f3f4f6;
            --color-text-primary: #111827;
            --color-text-secondary: #4b5563;
            --color-text-tertiary: #9ca3af;
            --color-text-info: #0C447C;
            --border-radius-lg: 12px;
        }

        .stApp {
            background: #ffffff;
            color: var(--color-text-primary);
            font-family: "Inter", sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6, p, div, span, label {
            font-family: "Inter", sans-serif;
        }

        [data-testid="block-container"] {
            max-width: 900px;
            padding: 0 !important;
            margin-top: 2rem;
            border: 0.5px solid var(--color-border-secondary);
            border-radius: var(--border-radius-lg);
            overflow: hidden;
            background: var(--color-background-tertiary);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        header[data-testid="stHeader"] {
            display: none;
        }

        .mock-bar {
            background: var(--color-background-secondary);
            border-bottom: 0.5px solid var(--color-border-tertiary);
            padding: 6px 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }

        div[data-testid="column"]:nth-child(1) {
            background: var(--color-background-primary);
            border-right: 0.5px solid var(--color-border-tertiary);
            padding: 8px 0 !important;
            margin: 0 !important;
            min-height: 500px;
        }
        
        div[data-testid="column"]:nth-child(2) {
            padding: 12px !important;
            background: var(--color-background-tertiary);
        }

        .s-logo {
            padding: 6px 10px 8px;
            border-bottom: 0.5px solid var(--color-border-tertiary);
            margin-bottom: 4px;
            font-size: 12px;
            font-weight: 600;
            color: var(--color-text-info);
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .s-logo i { font-size: 13px; }

        div[role="radiogroup"] { gap: 2px; }
        div[role="radiogroup"] label {
            background: transparent;
            border-left: 2px solid transparent;
            border-radius: 0;
            padding: 6px 10px;
            margin: 0 !important;
            transition: none;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        div[role="radiogroup"] label p { font-size: 12px !important; color: var(--color-text-secondary) !important; margin: 0; font-weight: 400 !important; }
        div[role="radiogroup"] label:hover { background: var(--color-background-secondary); }
        div[role="radiogroup"] label[data-selected="true"] { background: var(--color-background-info); border-left-color: #185FA5; }
        div[role="radiogroup"] label[data-selected="true"] p { color: var(--color-text-info) !important; font-weight: 600 !important; }
        div[role="radiogroup"] [data-baseweb="radio"] > div:first-child { display: none !important; }

        div[role="radiogroup"] label:nth-child(1)::before { content: "\\eb34"; font-family: 'tabler-icons'; font-size: 12px; color: inherit; }
        div[role="radiogroup"] label:nth-child(2)::before { content: "\\ea60"; font-family: 'tabler-icons'; font-size: 12px; color: inherit; }
        div[role="radiogroup"] label:nth-child(3)::before { content: "\\eefd"; font-family: 'tabler-icons'; font-size: 12px; color: inherit; }
        div[role="radiogroup"] label:nth-child(4)::before { content: "\\eff6"; font-family: 'tabler-icons'; font-size: 12px; color: inherit; }
        div[role="radiogroup"] label:nth-child(5)::before { content: "\\ea0b"; font-family: 'tabler-icons'; font-size: 12px; color: inherit; }

        .card-m { background: var(--color-background-primary); border: 0.5px solid var(--color-border-tertiary); border-radius: 8px; padding: 10px 12px; margin-bottom: 8px; }
        .card-label { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: .07em; color: var(--color-text-tertiary); margin-bottom: 6px; }
        
        .chip-m { display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; background: var(--color-background-info); color: #0C447C; border: 0.5px solid #B5D4F4; border-radius: 20px; font-size: 13px; }
        .row-m { display: flex; gap: 8px; }
        .col-m { flex: 1; margin-bottom: 0; }
        .mini-card { background: var(--color-background-secondary); border-radius: 6px; padding: 6px 8px; font-size: 13px; }
        .mini-card-val { font-size: 14px; font-weight: 600; color: var(--color-text-primary); margin-top: 2px; }
        .mini-bar-m { height: 3px; background: var(--color-border-tertiary); border-radius: 2px; margin-top: 3px; overflow: hidden; }
        .mini-fill-m { height: 100%; border-radius: 2px; }
        .tag-m { display: inline-flex; align-items: center; gap: 3px; padding: 2px 6px; border-radius: 20px; font-size: 13px; font-weight: 500; }
        .tag-green { background: #EAF3DE; color: #27500A; }
        .tag-amber { background: #FAEEDA; color: #633806; }
        .tag-red { background: #FCEBEB; color: #791F1F; }
        .tag-blue { background: #E6F1FB; color: #0C447C; }
        .badge-m { display: inline-block; padding: 2px 8px; border-radius: 20px; font-size: 13px; font-weight: 500; }
        .badge-maybe { background: #FAEEDA; color: #633806; }
        .badge-yes { background: #EAF3DE; color: #27500A; }
        .badge-no { background: #FCEBEB; color: #791F1F; }
        .screen-num { display: inline-flex; align-items: center; justify-content: center; width: 20px; height: 20px; border-radius: 50%; background: var(--color-background-info); color: #0C447C; font-size: 12px; font-weight: 600; margin-right: 6px; flex-shrink: 0; }
        .screen-header { display: flex; align-items: center; margin-bottom: 8px; }
        .screen-label { font-size: 13px; font-weight: 500; color: var(--color-text-tertiary); text-transform: uppercase; letter-spacing: .08em; }
        .override-big { font-size: 22px; font-weight: 600; color: var(--color-text-primary); }
        .hr-final-m { display: flex; align-items: center; gap: 10px; padding: 8px; background: var(--color-background-secondary); border-radius: 6px; border: 0.5px solid var(--color-border-tertiary); margin-bottom: 8px;}

        /* Streamlit components */
        .stButton button, .stFormSubmitButton button { border-radius: 6px !important; border: 0 !important; background: #185FA5 !important; color: #E6F1FB !important; font-weight: 500 !important; padding: 5px 10px !important; font-size: 13px !important; min-height: 0 !important; line-height: normal !important; display: inline-flex; align-items: center; justify-content: center; gap: 4px; box-shadow: none !important;}
        .stButton button p, .stFormSubmitButton button p { margin: 0 !important; display: inline-flex; align-items: center; }
        .stButton button::before, .stFormSubmitButton button::before { content: "\\eb29"; font-family: 'tabler-icons'; font-size: 13px; margin-right: 4px; display: inline-block; }
        
        /* Specific override for "Save HR Decision" button icon */
        .stButton button[kind="primary"]::before { content: "\\ea8e"; } /* ti-device-floppy */

        .stTextArea textarea, .stTextInput input { border-radius: 6px !important; border: 0.5px solid var(--color-border-secondary) !important; background: var(--color-background-primary) !important; color: var(--color-text-primary) !important; font-size: 13px !important; padding: 4px 6px !important; box-shadow: none !important;}
        
        [data-testid="stFileUploadDropzone"] { border: 1px dashed var(--color-border-secondary) !important; border-radius: 6px !important; background-color: var(--color-background-secondary) !important; padding: 10px !important; text-align: center; }
        [data-testid="stFileUploadDropzone"] * { color: var(--color-text-primary) !important; }
        .stFileUploader div[data-testid="stMarkdownContainer"] p { font-size: 13px !important; color: var(--color-text-tertiary) !important; }
        
        .stSlider [data-baseweb="slider"] { padding-top: 0; padding-bottom: 0; }
        .stSlider [data-baseweb="slider"] > div:nth-child(1) { background: var(--color-border-tertiary); height: 3px;}
        .stSlider [data-baseweb="slider"] > div:nth-child(2) { background: #185FA5; height: 3px; }
        
        .stExpander { border: 0.5px solid var(--color-border-tertiary) !important; border-radius: 6px !important; background: var(--color-background-primary) !important; margin-bottom: 4px !important;}
        .stExpander summary { font-size: 13px !important; font-weight: 500 !important; color: var(--color-text-primary) !important; padding: 6px 8px !important; }
        .stExpander div[role="region"] { background: var(--color-background-secondary); padding: 6px 8px 8px !important; font-size: 13px !important; color: var(--color-text-secondary) !important; line-height: 1.6;}
        
        /* Hide markdown gaps */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlockBorderWrapper"] { padding: 0 !important; }
        .element-container { margin-bottom: 0 !important; }
        
        </style>
        """,
        unsafe_allow_html=True,
    )

def set_active_tab(tab_name):
    st.session_state.nav_selection = tab_name

def extract_resume_text(uploaded_file):
    file_type = uploaded_file.name.lower().split(".")[-1]
    if file_type == "pdf":
        uploaded_file.seek(0)
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "".join(page.get_text() for page in document)
        document.close()
        return text
    if file_type == "docx":
        uploaded_file.seek(0)
        document = docx.Document(uploaded_file)
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    return ""

def format_file_size(size_in_bytes):
    if not size_in_bytes:
        return "0 KB"
    return f"{round(size_in_bytes / 1024, 1)} KB"

def badge_class(label):
    normalized = label.lower()
    if normalized == "hire":
        return "badge-yes"
    if normalized == "reject":
        return "badge-no"
    return "badge-maybe"

def recommendation_from_score(score):
    if score >= 75:
        return "Hire"
    if score >= 55:
        return "Maybe"
    return "Reject"

def progress_ring(score_value, size=64, stroke_width=6):
    radius = (size / 2) - stroke_width
    circumference = 2 * 3.14159 * radius
    percent = max(0, min(100, float(score_value)))
    dash_offset = circumference * (1 - percent / 100)
    score_text = int(round(percent))

    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" role="img" aria-label="Score ring">
        <circle cx="{size / 2}" cy="{size / 2}" r="{radius}" fill="none" stroke="var(--color-border-tertiary)" stroke-width="{stroke_width}"></circle>
        <circle
            cx="{size / 2}"
            cy="{size / 2}"
            r="{radius}"
            fill="none"
            stroke="#185FA5"
            stroke-width="{stroke_width}"
            stroke-dasharray="{circumference}"
            stroke-dashoffset="{dash_offset}"
            stroke-linecap="round"
            transform="rotate(-90 {size / 2} {size / 2})"
        ></circle>
        <text x="50%" y="45%" text-anchor="middle" font-size="13" font-weight="500" fill="var(--color-text-primary)">{score_text}</text>
        <text x="50%" y="62%" text-anchor="middle" font-size="8" fill="var(--color-text-secondary)">/100</text>
    </svg>
    """

def render_empty_state(message):
    st.markdown(
        f"<div class='card-m' style='text-align:center;color:var(--color-text-tertiary);font-size: 13px;'>{html.escape(message)}</div>",
        unsafe_allow_html=True,
    )

def analyze_candidate(jd_text, uploaded_resume):
    resume_text = extract_resume_text(uploaded_resume)
    jd = jd_agent(jd_text)
    resume = resume_agent(resume_text)

    jd_embedding = embedding_agent(str(jd))
    resume_embedding = embedding_agent(str(resume))

    score = scoring_agent(jd, resume, jd_embedding, resume_embedding)
    analysis = analysis_agent(jd, resume, score)
    questions = interview_agent(jd, resume)

    return {
        "jd": jd,
        "resume": resume,
        "score": score,
        "analysis": analysis,
        "questions": questions,
        "resume_text": resume_text,
    }

def render_header():
    tab_number = TABS.index(st.session_state.nav_selection) + 1
    render_html(f"""
        <div class="screen-header">
            <span class="screen-num">{tab_number}</span>
            <span class="screen-label">{html.escape(st.session_state.nav_selection)} tab</span>
        </div>
        """)

def render_sidebar():
    st.markdown(
        """
        <div class="s-logo"><i class="ti ti-robot" aria-hidden="true"></i>AI HR ATS</div>
        """,
        unsafe_allow_html=True,
    )
    selected_tab = st.radio(
        "Navigation",
        TABS,
        index=TABS.index(st.session_state.nav_selection),
        label_visibility="collapsed",
    )
    
    if selected_tab != st.session_state.nav_selection:
        st.session_state.nav_selection = selected_tab
        st.rerun()

def render_job_description_tab():
    render_html("<div class='card-m'><div class='card-label'>Job description</div>")
    with st.form("analysis_form", clear_on_submit=False):
        st.text_area(
            "Job Description",
            key="jd_text_input",
            label_visibility="collapsed",
            height=40,
            placeholder="Paste the job description here...",
        )
        st.markdown("</div><div class='card-m'><div class='card-label'>Resume upload</div>", unsafe_allow_html=True)
        
        uploaded_resume = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx"],
            key="resume_upload",
            label_visibility="collapsed",
        )

        if uploaded_resume is not None:
            st.session_state.resume_file_name = uploaded_resume.name
            st.session_state.resume_file_size = uploaded_resume.size
            st.markdown(
                f"<div style='margin-top:6px'><div class='chip-m'><i class='ti ti-file-type-pdf' style='font-size: 13px'></i>{html.escape(uploaded_resume.name)} · {format_file_size(uploaded_resume.size)} <i class='ti ti-check' style='font-size: 12px'></i></div></div>",
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Analyse with AI")

    if submitted:
        jd_text = st.session_state.jd_text_input.strip()
        resume_file = st.session_state.get("resume_upload")

        if not jd_text or resume_file is None:
            st.warning("Add the job description and upload a PDF or DOCX resume before starting the analysis.")
        else:
            try:
                st.session_state.candidate_id = str(uuid.uuid4())
                with st.spinner("Analyzing candidate and preparing all tabs..."):
                    st.session_state.result = analyze_candidate(jd_text, resume_file)

                ai_total = float(st.session_state.result["score"].total_score)
                st.session_state.final_score = ai_total
                st.session_state.override_score = int(round(ai_total))
                st.session_state.override_reason_text = ""
                st.session_state.override_feedback = ""
                set_active_tab("AI Score")
                st.rerun()
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")

def render_score_tab():
    result = st.session_state.result
    if not result:
        render_empty_state("Run the analysis from the Job Description tab to see the AI score, subscores, JD match, and confidence.")
        return

    score = result["score"]
    recommendation = score.recommendation or recommendation_from_score(score.total_score)

    cards = []
    for label, field_name, color in SUBSCORE_META:
        value = round(float(getattr(score, field_name, 0)), 1)
        cards.append(textwrap.dedent(f"""
            <div class="mini-card">
                <div style="font-size: 13px;color:var(--color-text-tertiary)">{html.escape(label)}</div>
                <div class="mini-card-val" style="font-size:12px">{value}/10</div>
                <div class="mini-bar-m">
                    <div class="mini-fill-m" style="width:{value * 10}%; background:{color};"></div>
                </div>
            </div>
            """))

    render_html(f"""
        <div class="card-m">
            <div class="card-label">AI generated score</div>
            <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
                <div style="display:flex;flex-direction:column;align-items:center;gap:4px">
                    {progress_ring(score.total_score)}
                    <span class="badge-m {badge_class(recommendation)}">{html.escape(recommendation)}</span>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px;flex:1;min-width:180px">
                    {''.join(cards)}
                </div>
            </div>
        </div>
        <div class="row-m">
            <div class="col-m card-m">
                <div class="card-label">JD match</div>
                <div style="font-size:18px;font-weight:500;color:#BA7517">{round(float(score.jd_match_score), 1)}%</div>
                <div style="font-size: 13px;color:var(--color-text-tertiary)">skills matched</div>
            </div>
            <div class="col-m card-m">
                <div class="card-label">Confidence</div>
                <div style="font-size:18px;font-weight:500">{html.escape(score.confidence_level)}</div>
                <div style="font-size: 13px;color:var(--color-text-tertiary)">model confidence</div>
            </div>
        </div>
        """)

def render_analysis_tab():
    result = st.session_state.result
    if not result:
        render_empty_state("Run the analysis first to see strengths, missing skills, and the AI summary.")
        return

    analysis = result["analysis"]
    score = result["score"]
    strengths = analysis.strengths or score.strengths
    weaknesses = analysis.weaknesses or score.weaknesses
    missing_skills = analysis.missing_skills

    strength_tags = "".join(
        f"<span class='tag-m tag-green'><i class='ti ti-check' style='font-size: 13px'></i>{html.escape(item)}</span>" for item in strengths
    ) or "<span class='tag-m tag-green'><i class='ti ti-check' style='font-size: 13px'></i>Strong foundation detected</span>"
    
    gap_tags = "".join(
        f"<span class='tag-m tag-amber'><i class='ti ti-alert-triangle' style='font-size: 13px'></i>{html.escape(item)}</span>" for item in missing_skills
    )
    weakness_tags = "".join(
        f"<span class='tag-m tag-red'><i class='ti ti-certificate-off' style='font-size: 13px'></i>{html.escape(item)}</span>" for item in weaknesses
    )
    tags_html = gap_tags + weakness_tags
    if not tags_html:
        tags_html = "<span class='tag-m tag-blue'>No major gaps surfaced</span>"

    recommendation = analysis.hiring_recommendation or score.recommendation
    focus_tags = "".join(
        f"<span class='tag-m tag-amber'>{html.escape(item)}</span>" for item in analysis.interview_focus
    )

    render_html(f"""
        <div class="card-m">
            <div class="card-label">Strengths</div>
            <div style="display:flex;flex-wrap:wrap;gap:4px">{strength_tags}</div>
        </div>
        <div class="card-m">
            <div class="card-label">Missing skills</div>
            <div style="display:flex;flex-wrap:wrap;gap:4px">{tags_html}</div>
        </div>
        <div class="card-m">
            <div class="card-label">AI analysis summary</div>
            <div style="font-size: 13px;color:var(--color-text-secondary);line-height:1.6">{html.escape(analysis.summary)}</div>
            <div style="margin-top:6px;display:flex;gap:5px">
                <span class="tag-m tag-blue">{html.escape(recommendation)}</span>
                {focus_tags}
            </div>
        </div>
        """)

def render_questions_tab():
    result = st.session_state.result
    if not result:
        render_empty_state("Run the analysis first to generate grouped interview questions.")
        return

    questions = result["questions"]
    render_html("<div class='card-m'><div class='card-label'>AI generated interview questions</div>")

    if not questions.sections:
        render_empty_state("No interview sections were generated for this candidate.")
    else:
        for index, section in enumerate(questions.sections):
            title = section.title or f"Section {index + 1}"
            with st.expander(f"📁 {title}", expanded=index == 0):
                for question_number, question in enumerate(section.questions, start=1):
                    st.markdown(f"{question_number}. {question}")

    st.markdown("</div>", unsafe_allow_html=True)


def progress_ring_small(score_value):
    size = 48
    stroke_width = 5
    radius = (size / 2) - stroke_width
    circumference = 2 * 3.14159 * radius
    percent = max(0, min(100, float(score_value)))
    dash_offset = circumference * (1 - percent / 100)
    score_text = int(round(percent))

    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" role="img" aria-label="Final score ring">
        <circle cx="{size / 2}" cy="{size / 2}" r="{radius}" fill="none" stroke="var(--color-border-tertiary)" stroke-width="{stroke_width}"></circle>
        <circle
            cx="{size / 2}"
            cy="{size / 2}"
            r="{radius}"
            fill="none"
            stroke="#185FA5"
            stroke-width="{stroke_width}"
            stroke-dasharray="{circumference}"
            stroke-dashoffset="{dash_offset}"
            stroke-linecap="round"
            transform="rotate(-90 {size / 2} {size / 2})"
        ></circle>
        <text x="50%" y="45%" text-anchor="middle" font-size="10" font-weight="500" fill="var(--color-text-primary)">{score_text}</text>
        <text x="50%" y="65%" text-anchor="middle" font-size="7" fill="var(--color-text-secondary)">/100</text>
    </svg>
    """

def render_override_tab():
    result = st.session_state.result
    if not result:
        render_empty_state("Run the analysis first, then use this tab to adjust the score and save an HR decision.")
        return

    score = result["score"]
    
    render_html("<div class='card-m'><div class='card-label'>Adjust score</div>")
    st.slider(
        "Override score",
        min_value=0,
        max_value=100,
        step=1,
        key="override_score",
        label_visibility="collapsed",
    )
    render_html(f"""
        <div style="height:3px;background:var(--color-border-tertiary);border-radius:2px;overflow:hidden;margin-top:-10px;">
            <div style="width:{st.session_state.override_score}%;height:100%;background:#185FA5;border-radius:2px"></div>
        </div>
        </div>
    """)

    render_html("<div class='card-m'><div class='card-label'>Reason for override</div>")
    st.text_area(
        "Reason for override",
        key="override_reason_text",
        height=32,
        label_visibility="collapsed",
        placeholder="Explain why the manual adjustment is justified...",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    final_recommendation = recommendation_from_score(float(st.session_state.override_score))
    feedback = st.session_state.override_feedback or ""
    
    render_html(f"""
        <div class="hr-final-m">
            {progress_ring_small(st.session_state.override_score)}
            <div>
                <span class="badge-m {badge_class(final_recommendation)}">{html.escape(final_recommendation)}</span>
                <div style="font-size: 13px;color:var(--color-text-tertiary);margin-top:4px">Reviewed by HR Panel</div>
                <div style="font-size: 13px;color:var(--color-text-secondary);margin-top:4px;font-style:italic">{"" if not feedback else "AI: " + html.escape(feedback)}</div>
            </div>
        </div>
    """)

    if st.button("Save HR Decision", type="primary"):
        reason = st.session_state.override_reason_text.strip()
        if not reason:
            st.error("A reason is required before saving the HR override.")
        else:
            try:
                with st.spinner("Validating and saving HR override..."):
                    validation = validate_override(
                        old_score=score.total_score,
                        new_score=st.session_state.override_score,
                        reason=reason,
                        analysis_summary=result["analysis"].summary,
                    )

                    st.session_state.final_score = float(st.session_state.override_score)
                    st.session_state.override_feedback = validation.ai_comment
                    log_override(
                        candidate_id=st.session_state.candidate_id,
                        old_score=score.total_score,
                        new_score=st.session_state.final_score,
                        reason=reason,
                        ai_comment=validation.ai_comment,
                    )
                st.success("HR override saved successfully.")
            except Exception as exc:
                st.error(f"Override validation failed: {exc}")

def render_main_content():
    current_tab = st.session_state.nav_selection

    if current_tab == "Job Description":
        render_job_description_tab()
    elif current_tab == "AI Score":
        render_score_tab()
    elif current_tab == "Analysis":
        render_analysis_tab()
    elif current_tab == "Questions":
        render_questions_tab()
    else:
        render_override_tab()


def main():
    init_session_state()
    inject_styles()
    render_header()
    
    st.markdown(
        """
        <div class="mock-bar">
            <span class="dot" style="background:#E24B4A"></span>
            <span class="dot" style="background:#EF9F27"></span>
            <span class="dot" style="background:#639922"></span>
            <span style="font-size: 13px;color:var(--color-text-tertiary);margin-left:8px">AI HR ATS System</span>
        </div>
        """, unsafe_allow_html=True)

    nav_col, content_col = st.columns([1, 4])
    with nav_col:
        render_sidebar()
    with content_col:
        render_main_content()


if __name__ == "__main__":
    main()
