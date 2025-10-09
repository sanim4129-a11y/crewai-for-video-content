Dynamic, instruction-driven CrewAI project for real video content (≤45 min) — design → implementation (complete, runnable plan)

This project uses CrewAI to generate video content up to 45 minutes long. The system is driven by a `user_instruction` object and is designed to be fully parametric.

## Architecture and Pipeline

The system follows a pipeline of agents, each with a specific responsibility:

1.  **Intake Agent**: Validates the user's instructions and creates a new project.
2.  **Planner Agent**: Breaks down the video into scenes and determines the duration of each scene.
3.  **FactCheck / RAG Agent**: Gathers and verifies facts for the video script (used for news, crypto, and STEM domains).
4.  **Script Agent**: Generates the script for each scene, including narration, shot descriptions, and interview prompts.
5.  **Storyboard Agent**: Converts the shot descriptions into image prompts for the VisualGen Agent.
6.  **AssetManager**: Gathers and manages assets for the video, such as stock footage and images.
7.  **VisualGen Agent**: Generates the visual content for the video, including images and video clips.
8.  **TTS Agent**: Converts the script into speech using ElevenLabs.
9.  **Motion/Lipsync Agent**: Applies lip-syncing to talking-head videos.
10. **Editor Agent**: Assembles the video, including audio, video, and text overlays.
11. **QC Agent**: Performs quality control checks on the final video.
12. **Publish Agent**: Publishes the video to the desired platform.

## Tools

The project uses a variety of tools to accomplish its tasks, including:

*   **Gemini**: Used for text generation.
*   **ElevenLabs**: Used for text-to-speech.
*   **RAGTool**: Used for retrieving information from documents.
*   **WebSearchTool**: Used for searching the web.
*   **VectorDB**: Used for storing and retrieving vector embeddings.
*   **ImageGenTool**: Used for generating images.
*   **VideoGenTool**: Used for generating video clips.
*   **FFmpegTool**: Used for video and audio editing.
*   **QCTool**: Used for quality control.
*   **LicenseCheckerTool**: Used for checking the licenses of stock assets.

## Getting Started

To get started with the project, you will need to:

1.  Install the dependencies listed in `requirements.txt`.
2.  Set up your environment variables. You will need to create a `.env` file in the root of the project and add the following variables:
    ```
    GOOGLE_API_KEY=<your-google-api-key>
    ELEVENLABS_API_KEY=<your-elevenlabs-api-key>
    ```
3.  Run the `main.py` file.

## Implementation Checklist

*   [x] Configure CrewAI credentials & tools: ImageGen, VideoGen, TTS, WebSearch/RAGTool, VectorDB, FFmpeg environment.
*   [x] Drop intake, planner, factcheck, script, storyboard, visual_gen, tts, motion, editor, qc, publish agent code into your crew.
*   [x] Provide API keys for external services via secure secrets.
*   [ ] Run pilot with 1 scene (duration_minutes: 3) to validate pipeline end-to-end.
*   [ ] Inspect QC report, tweak prompts & image prompt engine parameters (seed, sampling) for consistent look.