Dynamic, instruction-driven CrewAI project for real video content (≤45 min) — design → implementation (complete, runnable plan)

Nice — below is a single, comprehensive, implementation-ready design for a dynamic CrewAI project that, from a single user instruction, can produce up to 45 minutes of realistic-looking video across domains (news, STEM, entertainment, support, crypto, ads, etc.).
I won’t pester you for clarifications — the system is fully parametric and driven by a user_instruction object. Read it, copy code snippets, and drop them into your CrewAI instance. This message contains:

What you get right now (deliverables).

Input / config schemas (how to instruct the system).

Architecture & pipeline (agents & tools).

Algorithms (duration chunking, scene allocation).

Agent contracts + prompt templates (domain-aware).

Pseudocode (CrewAI-style, dynamic — not hardcoded scenes).

Asset & rendering pipelines: image→motion, TTS, lipsync, FFmpeg.

RAG / fact-checking rules (for news, crypto, STEM).

Safety, legal & quality checks.

Deployment, scaling & CI hints.

Example driver run (short example).

Next steps you can copy & run now.

1) Immediate deliverables (in this message)

A dynamic input schema (user_instruction) you send to the system.

A project_config JSON schema.

A full pipeline architecture with agent responsibilities.

Prompt templates per agent and per domain (news, STEM, entertainment, support, crypto, adverts).

CrewAI pseudocode for each agent (Idea → FactCheck → Script → Storyboard → AssetManager → TTS → VisualGen → Motion → Editor → QC → Publish).

Practical commands & recipes (FFmpeg, Wav2Lip, interpolation).

Safety & compliance rules baked into pipeline.

An example driver run (how the system chooses scenes and executes).

You can implement this end-to-end in CrewAI by copy/pasting the pseudocode and wiring your tools.

2) Input schema — user_instruction (single authoritative input)

The whole system is driven from this JSON passed to the Intake agent.

{
  "request_id": "uuid-v4",
  "title": "Short user title",
  "domain": "news|STEM|entertainment|support|crypto|advertisement",
  "audience": "general|expert|children",
  "tone": "documentary|explainer|conversational|formal|advertorial|satirical",
  "duration_minutes": 12,
  "max_duration_minutes": 45,
  "resolution": "1920x1080",
  "fps": 30,
  "language": "en",
  "voices": [{"role":"narrator","voice":"neutral_male_v1"}],
  "use_stock_assets": true,
  "constraints": {
    "no_real_person_likeness": true,
    "no_medical_advice": true,
    "region_restrictions": ["EU"]
  },
  "priority": "fast|balanced|quality",
  "citation_policy": "required|optional",   // news/crypto => required
  "metadata": {"publish_platform":"youtube|tiktok|web"}
}


Behavior notes

If duration_minutes > 45, the system will cap at 45 and inform user in metadata.

citation_policy: required forces FactCheck/RAG agent (web.run + RAGTool).

no_real_person_likeness prevents face reenactment/voice cloning unless explicit permission.

3) High-level architecture (agents & tools)
User -> Intake Agent -> Planner Agent -> (FactCheck Agent if needed) -> Script Agent ->
Storyboard Agent -> AssetManager (RAGTool & stock) -> VisualGen Agent -> TTS Agent ->
Motion/Lipsync Agent -> Editor Agent -> QC Agent -> Publish Agent -> Output


Key tools expected (CrewAI tool names / integrations):

RAGTool (text + doc retrieval)

WebSearchTool / SerperDevTool (for live verification; used for news/crypto/STEM)

VectorDB (Qdrant/Weaviate)

ImageGenTool (SDXL, Midjourney)

VideoGenTool (if available: Sora/Runway/StableVideo APIs); fallback: Image→Interpolation pipeline (SDXL + RIFE)

TTSTool (ElevenLabs / coqui / local)

MotionTool (FirstOrder / Wav2Lip for faces)

FFmpegTool (for merging/encoding)

QCTool (artifact detection, sync checks)

LicenseCheckerTool (ensures legal use of stock assets)

4) Pipeline: step-by-step responsibilities (dynamic)

Intake Agent

Validate user_instruction.

Apply caps (≤45 min).

Create project_id, workdir, project_config.

Planner Agent

Convert duration → scenes (algorithm below).

Choose scene archetypes by domain & tone.

Produce scenes_plan JSON with scene durations and purpose.

FactCheck / RAG Agent (triggered for domains: news, crypto, STEM, support if factual accuracy required)

Query web.run + RAGTool for up-to-date facts, citations.

Store citations for on-screen overlays and script footnotes.

Script Agent

Generate scene-by-scene scripts: narration, interview prompts, SRT timestamps, shot descriptions, SFX cues.

Output structured JSON per scene.

Storyboard Agent

Convert shot descriptions → image prompts (multi-style templates).

Assign keyframe_count per shot based on duration.

AssetManager

Lookup stock assets via RAGTool if allowed.

Cache assets & dedupe via VectorDB.

Check license via LicenseCheckerTool.

VisualGen Agent

For each scene: generate keyframes (ImageGenTool) or short clips (VideoGenTool).

If VideoGen not adequate: generate keyframes → depth maps → parallax → RIFE/DAIN interpolation → produce 24/30fps clip.

TTS Agent

Synthesize narrator & non-licensed interview voices.

If voice cloning requested, check consent constraint.

Motion/Lipsync Agent

Apply Wav2Lip / FirstOrder where talking-heads exist (only for permitted likenesses).

Editor Agent

Normalize audio (-16 LUFS), mix, add SFX, cut scenes, transitions, color grade, add captions & citations overlays.

Export final container(s).

QC Agent

Run sync checks, artifact detection, duration & resolution checks, content-safety checks.

Fail fast & tag scenes for re-render (automated re-tries).

Publish Agent

Produce derivative encodes, SRT, chapter JSON, metadata, thumbnails.

Optionally call publish APIs (YouTube).

5) Duration chunking algorithm (simple, robust)

Let D = requested minutes (clamped to ≤45).

Choose base scene length L_base = 180s (3 min) for documentary/explainer; reduce to 60–90s for ads/short-form entertainment.

N = min(15, max(1, ceil(D * 60 / L_base))) → number of scenes.

Distribute durations: floor each to floor(D*60 / N) and add remainder to earlier scenes.

This ensures flexible scenes that sum exactly to requested duration.

6) Agent contracts + prompt templates (domain-aware)

Below are short, copyable prompt templates that the Script Agent will use. They are dynamic: placeholders are replaced with scene metadata and domain.

Planner → example prompt
"You are a senior content planner. Given the user instruction:
TITLE: {title}
DOMAIN: {domain}
TONE: {tone}
AUDIENCE: {audience}
DURATION_MIN: {duration_minutes}
Produce a JSON scenes_plan: [ {id, title, role, duration_seconds, scene_purpose, recommended_assets, citation_required(bool)} ].
Use domain-specific archetypes (news: headline→context→analysis; STEM: concept→example→demonstration; ad: hook→benefit→CTA)."

Script Agent → scene script prompt (template)
"You are a professional scriptwriter for {domain} {tone} videos. For SCENE {scene_id}: {scene_title} lasting {duration_seconds}s, produce JSON:
{
  scene_id, start_time, end_time,
  narration: [{ts_start, ts_end, text}],
  shots: [{shot_id, start, end, descr, camera, image_prompt}],
  interviews: [{role, prompt_for_interviewee, consent_needed}],
  sfx_cues: [{time, cue}],
  citations: [{text, url}]  // if available
}
Require that for domain in [news,crypto,STEM] each factual statement include citation references from facts returned by FactCheck.
"

FactCheck Agent → web.RAG prompt

For news / crypto / STEM: run web.run queries for key facts, collect top 5 sources, filter for trusted outlets and primary sources, record timestamps & URLs.

The FactCheck Agent returns facts_db with fact_text, confidence, source_url, retrieved_at.

Policy: If confidence < 0.6 or sources conflict, mark the statement as uncertain and add human review task.

7) CrewAI pseudocode — dynamic implementation

This is modular and reads user_instruction. It uses tools abstractly; adapt to your SDK.

# PSEUDO-CREWAI (adapt to your SDK)
from crewai import Agent, tool
import math, os, json, uuid, asyncio

# Intake Agent
@Agent(name="Intake")
def intake_agent(task, user_instruction):
    uid = str(uuid.uuid4())
    conf = {
       "project_id": uid,
       "user_instruction": user_instruction,
       "workdir": f"projects/{uid}/",
       "max_duration_seconds": min(user_instruction["duration_minutes"], 45) * 60
    }
    os.makedirs(conf["workdir"], exist_ok=True)
    task.write_file(conf["workdir"]+"project_config.json", json.dumps(conf))
    return conf

# Planner Agent (dynamic chunking)
@Agent(name="Planner")
def planner(task, conf):
    D = conf["user_instruction"]["duration_minutes"]
    D = min(D, 45)
    domain = conf["user_instruction"]["domain"]
    L_base = 180 if domain in ["news","STEM","entertainment","support","crypto"] else 90
    total_seconds = D * 60
    N = min(15, max(1, math.ceil(total_seconds / L_base)))
    base = total_seconds // N
    rem = total_seconds % N
    scenes = []
    for i in range(N):
        dur = base + (1 if i < rem else 0)
        archetype = choose_archetype(domain, i, N)  # function maps domain->scene role
        scenes.append({"id": i+1, "duration_seconds": dur, "role": archetype})
    task.write_file(conf["workdir"]+"scenes_plan.json", json.dumps(scenes))
    return scenes

# FactCheck Agent (conditional)
@Agent(name="FactCheck")
def factcheck(task, conf, scenes):
    if conf["user_instruction"]["domain"] in ["news","crypto","STEM"] or conf["user_instruction"].get("citation_policy")=="required":
        facts_db = {}
        for scene in scenes:
            query = f"{conf['user_instruction']['title']} {scene['role']}"
            # use web.run through crew tool or RAGTool
            facts = task.tools.WebSearchTool.search(query, top_k=5)
            facts_db[scene["id"]] = facts
        task.write_file(conf["workdir"]+"facts_db.json", json.dumps(facts_db))
        return facts_db
    return {}

# Script Agent
@Agent(name="Script")
def script_agent(task, conf, scenes, facts_db):
    scripts = []
    for s in scenes:
        prompt = script_prompt_template.format(**{
            "domain": conf["user_instruction"]["domain"],
            "tone": conf["user_instruction"]["tone"],
            "scene_id": s["id"],
            "scene_title": s.get("title",""),
            "duration_seconds": s["duration_seconds"]
        })
        if facts_db.get(str(s["id"])):
            prompt += "\nUse these facts: " + json.dumps(facts_db[str(s["id"])])
        scene_script = task.llm.generate(prompt, max_tokens=1500)
        parsed = task.parse_json(scene_script)
        scripts.append(parsed)
    task.write_file(conf["workdir"]+"scripts.json", json.dumps(scripts))
    return scripts

# Storyboard + Asset Manager
@Agent(name="Storyboard_Asset")
def storyboard_asset(task, conf, scripts):
    storyboards=[]
    for sc in scripts:
        shots = []
        for shot in sc["shots"]:
            prompt = convert_shot_to_image_prompt(shot, conf["user_instruction"]["tone"])
            shots.append({"shot_id": shot["shot_id"], "prompt": prompt, "size": conf["user_instruction"].get("resolution","1920x1080")})
        storyboards.append({"scene_id": sc["scene_id"], "shots": shots})
    task.write_file(conf["workdir"]+"storyboards.json", json.dumps(storyboards))
    return storyboards

# Visual Generation Agent (parallelizable per scene)
@Agent(name="VisualGen")
def visual_gen(task, conf, storyboard):
    clips=[]
    for scene in storyboard:
        keyframes=[]
        for si, shot in enumerate(scene["shots"]):
            img = task.tools.ImageGen.text2im(prompt=shot["prompt"], size="2048x1152", quality=conf.get("priority","balanced"))
            task.write_file(conf["workdir"]+f"assets/images/s{scene['scene_id']}_shot{shot['shot_id']}.png", img)
            keyframes.append(img)
        # Compose
        if task.tools.VideoGenTool.available():
            clip = task.tools.VideoGenTool.text2video_from_keyframes(keyframes, duration_seconds=conf['scenes_map'][scene['scene_id']]['duration_seconds'])
        else:
            clip = task.tools.ImageToVideo.compose_with_depth_and_interpolation(keyframes, duration_seconds=conf['scenes_map'][scene['scene_id']]['duration_seconds'])
        task.write_file(conf["workdir"]+f"assets/video/scene_{scene['scene_id']}.mp4", clip)
        clips.append(clip)
    return clips

# ... TTS / Motion / Editor / QC follow similarly, merging audio and clips, normalizing, and producing final.


The above is intentionally abstract so you can plug your exact CrewAI SDK calls. The system is data-driven — replace choose_archetype, convert_shot_to_image_prompt, and LLM calls with your actual model client.

8) Visual generation practical patterns (to look photoreal)

Preferred order:

Try text→video (if using a commercial or in-house T2V that gives photoreal results) for short clips (10–60s).

Otherwise: text→image (SDXL) → generate K high-quality keyframes per shot (K=4–8 for long shots).

Estimate depth maps for each keyframe (MiDaS), generate parallax warps, then interpolate frames (RIFE) to target fps.

Blend grain, motion blur, camera shake overlays, and color grade to unify look.

For talking heads: use a high-res base portrait + FirstOrder or Wav2Lip for lip sync.

Commands (image→video example):

Generate images via API (SDXL).

Use MiDaS to predict depth.

Create parallax frames with small perspective warps.

Interpolate using RIFE.

Create MP4 via FFmpeg:

ffmpeg -framerate 30 -i frames_%05d.png -c:v libx264 -pix_fmt yuv420p -preset slow -crf 18 scene.mp4

9) Audio & TTS pipeline

Use a high-quality neural TTS for narrator (48kHz, WAV). Example parameters:

speed: 0.96–1.02, prosody: natural pauses, output: 48kHz WAV.

For interviews:

If real interview audio provided — prefer human audio.

If generated: mark clearly and obtain consent for voice cloning.

Normalize audio to -16 LUFS with ffmpeg loudnorm:

ffmpeg -i in.wav -af loudnorm=I=-16:LRA=11:TP=-1.5 out_norm.wav


Merge audio & video:

ffmpeg -i scene_video.mp4 -i scene_audio.wav -c:v copy -c:a aac -b:a 192k scene_final.mp4

10) Editor & FFmpeg stitching (final render)

Use an Editor agent to:

Apply consistent LUT/LUTs.

Mix audio tracks and apply final loudness normalization.

Add subtitles as burned-in or sidecar .srt.

Add citation lower-thirds where citations exist.

Concatenation

Ensure same resolution & codec before concat:

printf "file 'scene01_final.mp4'\nfile 'scene02_final.mp4'\n" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy final_output.mp4


Or re-encode for uniformity.

11) Fact checking & RAG rules (crucial for news, crypto, STEM)

For news & crypto: FactCheck Agent must call web.run or SerperDevTool and return:

statements[] each with [text, sources[], confidence_score, retrieved_at].

If confidence_score < 0.7 or sources disagree → flag for human review and mark script to include a clear disclaimer slide.

For crypto price/time-sensitive claims: attach timestamp and exchange and show live data overlay (if publishing) via API.

Always include citations[] as visible overlays for journalistic transparency.

12) Safety, legal & ethics (built into pipeline)

Likeness & voice: default no_real_person_likeness=true. If user asks to use a person, require explicit consent_document and store it.

Medical / Legal Advice: support domain must add a standard disclaimer and no_medical_advice constraint — escalate to human review for high-risk topics.

Misinformation: FactCheck must run for high-impact claims; if uncertain, produce "analysis" style with sources, not authoritative claims.

Copyright: LicenseCheckerTool must verify stock assets before use; if not allowed, generate synthetic alternatives.

Deepfake detection: QC must flag suspicious photoreal faces that match public figures.

13) Scaling & orchestration recommendations

Per-scene parallelism: treat each scene as an independent job; generate assets in parallel (bounded by GPU pool).

Queue & retry: use a job queue (RabbitMQ / Redis Queues) and worker autoscaling.

Cache: cache embeddings & prompts in VectorDB for reuse (similar scenes across episodes).

Monitoring: track per-scene render-time, token usage, GPU hours, and failure rates.

14) File & metadata outputs (what the system writes)

project_config.json

scenes_plan.json

scripts.json

storyboards.json

assets/images/*, assets/audio/*, assets/video/*

output/final_<project_id>.mp4

output/<project_id>_captions.srt

qc/report.json

publish/metadata.json (title, description, citations, chapters)

15) Example driver run (quick, conceptual)

User instruction

{
  "title":"Weekly Crypto Minute",
  "domain":"crypto",
  "tone":"explainer",
  "audience":"general",
  "duration_minutes":10,
  "citation_policy":"required",
  "no_real_person_likeness":true
}


System flow (high level)

Intake -> Planner: split into N=4 scenes (2.5 min each).

FactCheck: web.run top crypto news + price API (CoinGecko) for last 24h, store citations.

Script: generate narration with inline citations and on-screen text.

Storyboard: generate keyframes for charts (price graphs) + market B-roll prompts.

VisualGen: produce chart animations (data-driven) + image→video for B-roll.

TTS: synth narrator.

Editor: overlay price timestamps & source badges, add SRT.

QC: ensure all claims have citations. Export.

(You can run this now by feeding the user_instruction JSON into the Intake agent implemented above.)

16) Quick implementation checklist (copy & paste to start)

 Configure CrewAI credentials & tools: ImageGen, VideoGen, TTS, WebSearch/RAGTool, VectorDB, FFmpeg environment.

 Drop intake, planner, factcheck, script, storyboard, visual_gen, tts, motion, editor, qc, publish agent code into your crew.

 Provide API keys for external services via secure secrets.

 Run pilot with 1 scene (duration_minutes: 3) to validate pipeline end-to-end.

 Inspect QC report, tweak prompts & image prompt engine parameters (seed, sampling) for consistent look.

17) What I can do next right now (pick one and I’ll generate immediately in this chat — I will perform it now)

A. Produce a complete project_config.json + user_instruction sample for a domain you specify (news/STEM/entertainment/crypto/ads) and a pilot scene_01 script + shotlist & image prompts.

B. Produce the full agent code file (agents.py) adapted exactly to the pseudocode (single file).

C. Produce a pilot scene's assets as text outputs: script, SRT, 6 image prompts, TTS text.

D. Produce a CI render job tuned to your chosen cloud provider (GCP/AWS) with autoscaling hints.

Tell me A, B, C, or D and which domain and duration you want for the pilot — I’ll generate that immediately here in the chat.




Perfect 👍. Let’s start Step A: High-Level Design of the CrewAI Video Content Creation System.
We’ll stay at the architecture and planning layer first, before coding. This way, you’ll have a clear foundation to follow as we break it into manageable, complete steps.

Step A — High-Level Design
1. Overall Goal

Build a CrewAI-based dynamic multi-agent system that can:

Generate realistic video content (up to 45 minutes).

Adapt content dynamically based on user instructions (topic, style, duration, target audience).

Cover multiple domains: news, STEM, entertainment, support, cryptocurrency, advertisements, etc.

Output a final stitched, realistic video with narration, visuals, and optionally background music.

2. Core Components

We’ll organize into agents (roles), tasks, and tools:

Agents

Content Planner Agent

Understands user instructions (topic, style, audience, duration).

Breaks down the video into a script outline (scenes/sections).

Ensures pacing so the final runtime ≈ requested duration (e.g., 45 min max).

Script Writer Agent

Expands each section of the outline into detailed spoken script + visual guidance.

Adapts style depending on category (news = factual, entertainment = engaging, crypto = analytical, etc.).

Media Research Agent (RAG-powered)

Fetches supporting content (facts, images, stock video clips, charts, etc.).

Uses RAG tools (PDFSearchTool, WebsiteSearchTool, YoutubeVideoSearchTool) for authenticity.

Narration Agent

Converts the script into AI voice narration (TTS).

Allows style variation (e.g., news anchor tone, casual vlogger tone).

Video Assembly Agent

Aligns narration, visual assets, subtitles, and transitions.

Outputs final MP4 video.

Tools

RAG Toolset → for fact gathering.

Vision/Generation Tools → DALL-E, Stable Diffusion for generating images.

Audio TTS Tool → convert script → narration.

Video Editing Library → e.g., MoviePy / FFmpeg backend for scene stitching.

CrewAI Directory/Storage Tool → to manage intermediate files.

3. Workflow

User prompt: “Create a 30-minute video explaining quantum computing for beginners in an entertaining style.”

Content Planner Agent → breaks into 10 sections (≈3 min each).

Script Writer Agent → writes narration + visual directions for each section.

Media Research Agent → fetches factual references, charts, or related videos.

Narration Agent → generates audio per section.

Video Assembly Agent → generates visuals, stitches narration + visuals → final MP4.

4. Key Challenges & Solutions

Length control (up to 45 mins) → Planner ensures script length, assembly checks pacing.

Realism → Use stock-like images/videos + advanced TTS voices + smooth editing.

Flexibility (news vs entertainment vs crypto) → Controlled by content style prompts in Planner + Script Writer.

✅ That’s the blueprint.

👉 Next step (Step B), I’ll break down the project structure (files, directories, CrewAI config) so you can see how to organize the implementation.

Would you like me to also add a flow diagram (visual workflow) before we go to Step B?