import json
from datetime import datetime

from config import llm
from override_model import OverrideValidationModel

LOG_FILE = "override_logs.json"
structured_llm = llm.with_structured_output(OverrideValidationModel)


def validate_override(old_score, new_score, reason, analysis_summary=""):
    prompt = f"""
    You are assisting an HR reviewer who manually adjusted an AI candidate score.

    Original score: {old_score}
    New score: {new_score}
    Reason: {reason}
    Analysis summary: {analysis_summary}

    Return:
    - is_reasonable
    - ai_comment

    Rules:
    - ai_comment must be one concise sentence.
    - Be supportive but honest.
    - Mention whether the override seems justified.
    """
    return structured_llm.invoke(prompt)


def log_override(candidate_id, old_score, new_score, reason, ai_comment=""):
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            logs = json.load(file)
    except Exception:
        logs = []

    logs.append(
        {
            "candidate_id": candidate_id,
            "old_score": old_score,
            "new_score": new_score,
            "reason": reason,
            "ai_comment": ai_comment,
            "timestamp": str(datetime.now()),
        }
    )

    with open(LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4)
