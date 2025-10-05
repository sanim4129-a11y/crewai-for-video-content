from crewai import Agent

narration_agent = Agent(
    role="Narration Generator",
    goal=(
        "Convert the completed script into high-quality audio narration "
        "using text-to-speech. Adapt voice to the chosen style (e.g., "
        "serious news anchor, casual vlogger, or professional trainer)."
    ),
    backstory=(
        "A skilled voice-over artist powered by AI TTS engines. Known for "
        "realistic delivery and consistent tone."
    ),
    verbose=True,
)
