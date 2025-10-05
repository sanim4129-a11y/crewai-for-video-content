# tests/test_narration.py

from crewai_project.agents import narration_agent
from crewai_project.tasks import narration_task

def test_narration():
    inputs = {"script": "This is a sample narration."}
    result = narration_agent.execute(narration_task, inputs)
    print("Narration file:", result)
    assert result.endswith(".wav")
