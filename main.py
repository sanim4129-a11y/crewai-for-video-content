# crewai_project/main.py

from crew import build_crewai_video_crew

if __name__ == "__main__":
    crew = build_crewai_video_crew()
    result = crew.kickoff(inputs={
        "topic": "Quantum Computing for Beginners",
        "style": "entertaining",
        "duration": 3  # minutes
    })
    print("✅ Video generated:", result)
# Entry point for running the Crew
