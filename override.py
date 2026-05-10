def override_agent(old_score, new_score, reason):
    return {
        "old_score": old_score,
        "new_score": new_score,
        "reason": reason
    }