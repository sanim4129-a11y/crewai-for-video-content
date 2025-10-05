# Task definitions
# crewai_project/tasks.py

from crewai import Task
from agents import (
    planner_agent, script_writer_agent,
    media_research_agent, narration_agent,
    video_assembly_agent
)

planning_task = Task(
    description=(
        "Analyze the user’s input (topic, style, duration). "
        "Break it down into a structured video outline with "
        "sections. Ensure pacing matches the requested duration."
    ),
    expected_output=(
        "A JSON outline with sections, each containing: "
        "title, target duration, and summary of content."
    ),
    agent=planner_agent,
)
script_task = Task(
    description=(
        "Take the outline and expand each section into a "
        "full narration script. Add visual direction notes "
        "for each part (e.g., scene description, images, "
        "charts)."
    ),
    expected_output=(
        "A structured script (JSON or Markdown) with: "
        "section title, narration text, visual directions."
    ),
    agent=script_writer_agent,
)


research_task = Task(
    description=(
        "Gather supporting media for the script. Use search "
        "tools and RAG to fetch facts, stock imagery, or "
        "charts that enhance each section. Provide references "
        "and links."
    ),
    expected_output=(
        "For each section: a set of references, suggested "
        "images/videos, and fact checks."
    ),
    agent=media_research_agent,
)

narration_task = Task(
    description=(
        "Convert the script into narration audio files. "
        "Generate one audio file per section, ensuring "
        "voice matches requested style."
    ),
    expected_output=(
        "A folder of audio files (e.g., MP3/WAV), one per section."
    ),
    agent=narration_agent,
)

assembly_task = Task(
    description=(
        "Take narration audio, visual assets, and script "
        "directions. Assemble into a final MP4 video with "
        "transitions and background music. Ensure runtime "
        "matches requested duration."
    ),
    expected_output=(
        "A polished MP4 video file not exceeding requested duration."
    ),
    agent=video_assembly_agent,
)
