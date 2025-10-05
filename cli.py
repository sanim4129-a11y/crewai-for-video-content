# crewai_project/cli.py
import argparse
from crewai_project.crew import build_crewai_video_crew

def main():
    parser = argparse.ArgumentParser(description="CrewAI Video Generator")
    parser.add_argument("--topic", required=True, help="Topic of the video")
    parser.add_argument("--style", default="educational", help="Style of video")
    parser.add_argument("--duration", type=int, default=10, help="Duration in minutes")
    args = parser.parse_args()

    crew = build_crewai_video_crew()
    result = crew.kickoff(inputs={
        "topic": args.topic,
        "style": args.style,
        "duration": args.duration
    })
    print("✅ Video created:", result)

if __name__ == "__main__":
    main()
