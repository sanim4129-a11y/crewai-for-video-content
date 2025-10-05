# crewai_project/crew.py

from crewai import Crew
from agents import (
    planner_agent, script_writer_agent,
    media_research_agent, narration_agent,
    video_assembly_agent
)
from tasks import (
    planning_task, script_task,
    research_task, narration_task,
    assembly_task
)

def build_crewai_video_crew():
    return Crew(
        agents=[
            planner_agent,
            script_writer_agent,
            media_research_agent,
            narration_agent,
            video_assembly_agent
        ],
        tasks=[
            planning_task,
            script_task,
            research_task,
            narration_task,
            assembly_task
        ],
        verbose=True,
        process="sequential"  # strict ordered pipeline
    )
