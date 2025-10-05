# crewai_project/api.py
from fastapi import FastAPI
from pydantic import BaseModel
from crewai_project.crew import build_crewai_video_crew

app = FastAPI()

class VideoRequest(BaseModel):
    topic: str
    style: str = "educational"
    duration: int = 10

@app.post("/generate_video/")
def generate_video(req: VideoRequest):
    crew = build_crewai_video_crew()
    result = crew.kickoff(inputs=req.dict())
    return {"video_path": result}
