# tests/test_pipeline.py

from crew import build_crewai_video_crew

def test_pipeline():
    crew = build_crewai_video_crew()
    result = crew.kickoff(inputs={
        "topic": "The Basics of Quantum Computing",
        "style": "educational",
        "duration": 2  # minutes (short test)
    })
    print("Final output:", result)
    assert result.endswith(".mp4")
