# OHC Dashboard Backend - QC Bot

AI-powered Call Quality Control (QC) pipeline for automatically auditing healthcare outbound calls.

## AI Agents & Analysis Nodes

The pipeline consists of specific analysis agents running in parallel, feeding into a final QC summarizer:

### 1. Data Processing
- **Transcript Generator**: Converts audio to text.
- **Call Diarization**: Separates OHC Agent vs. Patient.

### 2. Analysis Agents (Parallel Execution)
- **Script Adherence**: Opening, closing, talking points.
- **Consent Capture**: Telehealth consent, HIPAA acknowledgment.
- **Qualification Completeness**: DOB, Insurance, Symptoms, Prior Auth.
- **Objection Handling**: Pricing, competitors, insurance checks.
- **Communication Quality**: Tone, empathy, clarity.
- **Keyword & Phrase Detection**: Required vs. prohibited keywords.
- **Sentiment Detection**: Frustration, confusion, risk.

### 3. Final Output
- **Final QC Report**: Aggregates all analysis to produce a final Score (0-100), executive summary, and critical flags.

## Pipeline Optimization
The LangGraph workflow is optimized for performance:
1. **Sequential data prep**: Transcription → Diarization
2. **Parallel Fan-Out**: All 7 analysis (quality/compliance) nodes run simultaneously.
3. **Fan-In**: The Final QC node waits for all parallel tasks to complete before generating the score.

## Technical Stack
- **Backend**: FastAPI (Python)
- **AI Orchestration**: LangGraph
- **Models**: GPT-4o / Gemini (via LangChain)
- **Task Management**: `uv`