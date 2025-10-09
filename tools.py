
# Custom tools integrations

# crewai_project/tools.py

from crewai.tools import BaseTool
from crewai_tools import (
    WebsiteSearchTool,
    PDFSearchTool,
    CSVSearchTool,
    YoutubeVideoSearchTool
)
from pydantic import Field
from typing import Any

# General web search
web_search_tool = WebsiteSearchTool()

# PDF document search
pdf_tool = PDFSearchTool()

# CSV structured data search
csv_tool = CSVSearchTool()

# YouTube video transcripts
yt_tool = YoutubeVideoSearchTool()

media_tools = [web_search_tool, pdf_tool, csv_tool, yt_tool]


import os
from elevenlabs import generate, save
from elevenlabs.client import ElevenLabs

class TextToSpeechTool(BaseTool):
    name: str = "Text to Speech Tool"
    description: str = "Converts text to speech and saves it as an audio file."
    voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # A default voice ID
    client: Any = Field(default_factory=lambda: ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY")))

    def _run(self, text: str, output_path: str) -> str:
        audio = generate(
            text=text,
            voice=self.voice_id,
            model="eleven_multilingual_v2"
        )
        save(audio, output_path)
        return output_path

tts_tool = TextToSpeechTool()

from moviepy import (
    VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips
)


class VideoAssemblyTool(BaseTool):
    name: str = "Video Assembly Tool"
    description: str = "Assembles video clips from images, audio, and script sections."

    def _run(self, script_sections: list, audio_paths: list, visual_assets: list, output_path: str) -> str:
        clips = []

        for i, section in enumerate(script_sections):
            # Load audio
            narration = AudioFileClip(audio_paths[i])

            # If we have an image asset
            if i < len(visual_assets):
                img_clip = ImageClip(visual_assets[i]).set_duration(narration.duration)
                img_clip = img_clip.set_audio(narration)
                clips.append(img_clip)
            else:
                # fallback: black screen with narration
                img_clip = ImageClip("black.jpg").set_duration(narration.duration)
                img_clip = img_clip.set_audio(narration)
                clips.append(img_clip)

        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        return output_path


video_tool = VideoAssemblyTool()
