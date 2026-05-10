def ranking_agent(candidates):
    return sorted(
        candidates,
        key=lambda x: x["score"],
        reverse=True
    )