from crewai import Agent
from llm import gemini_llm

script_writer_agent = Agent(
    role="Script Writer",
    goal=(
        "Expand each section of the outline into detailed narration text "
        "and visual scene directions, adapting to the requested style "
        "(news, STEM, entertainment, crypto, etc.)."
    ),
    backstory=(
        "A professional video scriptwriter who crafts engaging narration "
        "and gives clear cues for visuals. Skilled at tailoring tone "
        "and pacing to the target audience."
    ),
    verbose=True,
    llm=gemini_llm,
)
