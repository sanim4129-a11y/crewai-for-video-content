# crewai_project/agents.py

from crewai import Agent
from config import MAX_VIDEO_DURATION

planner_agent = Agent(
    role="Content Planner",
    goal=(
        "Break down the user’s instructions into a structured video outline "
        "with sections that align to the requested duration (up to "
        f"{MAX_VIDEO_DURATION//60} minutes)."
    ),
    backstory=(
        "An experienced video director who knows how to pace educational, "
        "entertaining, and professional video content. Ensures proper "
        "flow, logical sequencing, and approximate length."
    ),
    verbose=True,
)
