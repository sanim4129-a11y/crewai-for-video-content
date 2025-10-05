# crewai_project/config.py

import os

LLM_MODEL = "gpt-4o-mini"   # can switch to groq, llama3, etc.
MAX_VIDEO_DURATION = 45 * 60  # seconds

# API keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
# Configuration (LLM, storage, settings)
