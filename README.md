# AI HR Screening Agent

## Intelligent Candidate Evaluation & Explainable Recruitment System

An AI-powered recruitment assistant designed to help HR teams evaluate candidates faster, more consistently, and with greater transparency.

Recruiters often spend hours manually screening hundreds of resumes, leading to fatigue, inconsistent evaluations, unconscious bias, and delayed hiring decisions. This project automates the first-level candidate screening process while keeping humans fully involved in final hiring decisions.

The system uses Large Language Models (LLMs), semantic matching, structured AI outputs, and explainable scoring to transform unstructured hiring data into actionable recruitment intelligence.

---

# Solution Overview

The AI HR Screening Agent automates the initial candidate screening workflow.

The system accepts:
* Job Descriptions (JD)
* PDF/DOCX resumes
* 
It then:

* Extracts structured hiring requirements
* Parses candidate resumes into structured profiles
* Performs semantic JD matching
* Generates candidate scores across multiple dimensions
* Explains strengths and missing skills
* Produces ranked shortlist recommendations
* Keeps HR teams in control with human-in-the-loop review

---

# Key Features

## JD Parser

Extracts:

* Skills
* Experience
* Qualifications
* Certifications

from unstructured job descriptions using LLM-powered structured extraction.

---

## Resume & LinkedIn Ingestion

Supports:

* PDF resumes
* DOCX resumes
* LinkedIn profile data

Automatically extracts:

* Skills
* Projects
* Education
* Certifications
* Experience
* Strengths & weaknesses

---

## Semantic Matching Engine

Unlike traditional ATS systems that rely on exact keyword matching, this platform uses:

* Embeddings
* LLM reasoning
* Semantic similarity analysis

This allows the system to understand contextual skill relationships.

Example:
"Generative AI" can match with "LLM Application Development" semantically.

---

## Explainable AI (Novelty Feature)

The platform does not just generate scores.

It explains:

* Why a candidate matched
* Candidate strengths
* Missing required skills
* Areas of concern
* Hiring recommendation reasoning

This improves recruiter trust and transparency.

---

## JD Match Score (Novelty Feature)

Each candidate receives a semantic JD compatibility score based on:

* Skill overlap
* Experience relevance
* Educational alignment
* Certifications
* Semantic similarity
* LLM reasoning

## Human-in-the-Loop Recruitment

Recruiters can:
* Override AI recommendations
* Flag candidate profiles
* Add review comments
* Re-score candidates manually

This ensures the AI assists recruiters rather than replacing them.

---

# System Architecture
<img width="1024" height="1536" alt="ChatGPT Image May 11, 2026, 03_53_09 PM" src="https://github.com/user-attachments/assets/af3a7860-1a3a-40fd-80fb-53c9f0322f8f" />

## Workflow Summary

1. Job Description is uploaded and parsed using the JD Parser AI.
2. Resumes and LinkedIn profiles are ingested and converted into structured candidate profiles.
3. Semantic Matching AI compares candidates against JD requirements using embeddings and LLM reasoning.
4. The Scoring Engine generates JD Match Scores, strengths, weaknesses, and explainable insights.
5. Candidates are ranked and shortlisted automatically.
6. HR teams review recommendations through the Human-in-the-Loop dashboard before final decisions.
 
# Scoring Rubric

| Dimension                  | Weight |
| -------------------------- | ------ |
| Technical Skills Match     | 30%    |
| Experience Relevance       | 25%    |
| Education Fit              | 10%    |
| Certifications             | 10%    |
| Projects & Achievements    | 15%    |
| Communication & Leadership | 10%    |

The weighted scores produce:
* Overall Match Percentage
* Candidate Ranking
* Hire / No-Hire Recommendation
* Confidence Score
---
# AI & LLM Workflow

## Structured Output Validation

The system uses:
* Pydantic
* LangChain Structured Outputs
* JSON Mode
This ensures all AI responses are:
* Machine-readable
* Consistent
* Validated
* Production-ready
---

## Resume Parsing Agent

Converts unstructured resumes into structured candidate profiles using AI.
Extracts:
* Skills
* Experience
* Education
* Projects
* Certifications
* Strengths
* Weaknesses

---
## JD Parsing Agent

Converts unstructured job descriptions into validated hiring intelligence.
Extracts:
* Required skills
* Experience expectations
* Qualifications
* Certifications

---

# Security & Reliability

## Hallucination Reduction
Uses:
* Structured outputs
* Pydantic validation
* JSON schema enforcement
* Human review workflows

---

## API Key Security
Sensitive API keys are managed using:

* `.env`
* `python-dotenv`
* `.gitignore`

---

## Prompt Injection Protection

The platform reduces prompt manipulation risks using:

* Input sanitisation
* Output validation
* Structured schemas

---

## Human Oversight

Final hiring decisions remain under recruiter control.

---

# LangSmith Integration

LangSmith is used for:
* LLM tracing
* Prompt monitoring
* Debugging
* Workflow observability
* Performance analysis

This improves reliability and production readiness.

---

# Tech Stack

## Backend

* Python
* FastAPI
* LangChain
* Pydantic

## AI / ML

* OpenAI GPT Models
* Sentence Transformers
* Embeddings
* Semantic Similarity

## Data Processing

* PyPDF
* python-docx
* SQLite Cache

## Monitoring

* LangSmith

## Frontend

* Streamlit / HTML / CSS / JAVASCRIPT

---

# Performance Optimisations

## LLM Caching

SQLite caching is used to:

* Reduce repeated API calls
* Improve response speed
* Lower inference cost

---
# Example Output

<img width="1920" height="1080" alt="Screenshot (274)" src="https://github.com/user-attachments/assets/0b59d339-9bc9-43c2-84b8-0a56a38064d4" />
<img width="1920" height="1080" alt="Screenshot (275)" src="https://github.com/user-attachments/assets/4994cb47-8f01-4b3d-989b-d395e80ff4c6" />
<img width="1920" height="1080" alt="Screenshot (276)" src="https://github.com/user-attachments/assets/56b98ed3-6247-4c61-b7b6-e05ea0e7c22f" />
<img width="1920" height="1080" alt="Screenshot (277)" src="https://github.com/user-attachments/assets/43c98f1b-a1b2-45e9-a425-ba9c9e5a5487" />
<img width="1920" height="1080" alt="Screenshot (278)" src="https://github.com/user-attachments/assets/357e1f3f-f7b1-4cc9-8dd3-28850b84aecb" />

# Novelty & Innovation

## Key Innovations

* Explainable AI for recruitment
* Semantic JD matching
* Missing skill detection
* Human-in-the-loop hiring workflow
* Structured AI outputs with validation
* Transparent scoring system

---

# Future Improvements

* Bias detection dashboard
* Multi-agent recruitment orchestration
* Voice interview analysis
* ATS integration
* Real-time recruiter collaboration
* Candidate chatbot assistant
* Role-based authentication

---

# Impact

This project helps organisations:

* Reduce recruiter workload
* Improve hiring consistency
* Increase transparency
* Accelerate candidate screening
* Enhance recruiter productivity
* Make AI-assisted hiring more trustworthy

---

# Conclusion

The AI HR Screening Agent combines LLMs, semantic search, explainable AI, and structured validation to create a modern recruitment intelligence system.

Rather than replacing recruiters, the platform empowers HR teams with faster, smarter, and more transparent candidate evaluation workflows.

---
