# tests/test_planner.py

from crewai_project.agents import planner_agent
from crewai_project.tasks import planning_task

def test_planner():
    inputs = {"topic": "Climate Change", "style": "documentary", "duration": 5}
    result = planner_agent.execute(planning_task, inputs)
    print("Planner output:", result)
    assert "sections" in result  # basic check
