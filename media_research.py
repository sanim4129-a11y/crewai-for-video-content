from crewai import Agent

media_research_agent = Agent(
    role="Media Researcher",
    goal=(
        "Gather supporting content (facts, charts, stock images, "
        "and clips) using retrieval tools (RAG, web search, "
        "and document parsing). Provide references and suggested "
        "media assets for each script section."
    ),
    backstory=(
        "An investigative researcher who ensures the content "
        "is accurate and visually supported with relevant material."
    ),
    verbose=True,
    tools=[]  # will connect later in tools.py
)
