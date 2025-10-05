# crewai_project/agents.py

# Import agent definitions from their respective files
from planner import planner_agent
from script_writer import script_writer_agent
from media_research import media_research_agent
from narration import narration_agent
from video_assembly import video_assembly_agent

# Import tools
from tools import media_tools, tts_tool, video_tool

# Assign tools to the imported agents
media_research_agent.tools = media_tools
narration_agent.tools = [tts_tool]
video_assembly_agent.tools = [video_tool]
