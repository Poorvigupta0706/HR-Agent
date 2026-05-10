import json
def report_agent(data):
    with open("reports/report.json", "w") as f:
        json.dump(data, f, indent=4)