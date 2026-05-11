import json
from datetime import datetime
LOG_FILE = "override_logs.json"
def log_override(candidate_id, old_score, new_score, reason):
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []
    logs.append({
        "candidate_id": candidate_id,
        "old_score": old_score,
        "new_score": new_score,
        "reason": reason,
        "timestamp": str(datetime.now())
    })
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)