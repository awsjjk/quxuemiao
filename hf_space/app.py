import json
import yaml
import sys
import os
from pathlib import Path

# Ensure ai_module is importable
sys.path.insert(0, str(Path(__file__).parent))

from ai_module.agent import MatchAgent
import gradio as gr

_agent = MatchAgent()

def match_demand(subject, grade, location, budget, description, requirements, candidates_json):
    try:
        candidates = json.loads(candidates_json)
    except Exception:
        return "Error: Invalid candidate data format"

    demand = {
        "subject": subject,
        "grade": grade,
        "location": location,
        "budget": float(budget or 0),
        "time_slots": [],
        "description": description,
        "requirements": requirements,
        "tags": []
    }

    results = _agent.match(demand, candidates)
    return json.dumps(results, ensure_ascii=False, indent=2)


demo = gr.Interface(
    fn=match_demand,
    inputs=[
        gr.Textbox(label="Subject"),
        gr.Textbox(label="Grade"),
        gr.Textbox(label="Location"),
        gr.Number(label="Budget (Yuan/hour)"),
        gr.Textbox(label="Demand Description", lines=3),
        gr.Textbox(label="Additional Requirements"),
        gr.Textbox(label="Candidate Tutors JSON", lines=10),
    ],
    outputs=gr.Textbox(label="Matching Results", lines=15),
    title="QuXuemiao AI Tutor Matching",
    description="AI-powered matching and scoring based on parent demand and candidate tutor profiles",
)

if __name__ == "__main__":
    demo.launch()
