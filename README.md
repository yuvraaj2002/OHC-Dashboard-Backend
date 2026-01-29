# OHC Dashboard Backend - QC Bot

AI-powered Call Quality Control (QC) pipeline for automatically auditing healthcare outbound calls.

## AI Agents & Analysis Nodes

The pipeline consists of several specialized agents (nodes) that analyze transcribed calls for compliance, quality, and performance:

- **Transcript Generator**: Converts raw audio recordings into text transcriptions for further processing.
- **Call Diarization**: Normalizes speaker roles into `OHC_REPRESENTATIVE` and `PATIENT` to ensure accurate context analysis.
- **Script Adherence**: Checks if the agent followed the required script, including opening, closing, and essential talking points.
- **Consent Capture**: Detects compliance-critical events such as telehealth consent explanation, verbal agreement, and HIPAA acknowledgment.
- **Objection Handling**: Evaluates how the agent addresses concerns regarding pricing, insurance, and competitors, and whether objections were resolved.
- **Communication Quality**: Evaluates agent performance based on tone (polite/professional), empathy, clarity, and avoidance of unauthorized medical advice or guarantees.
- **Keyword & Phrase Detection**: A rules-engine agent that flags missing required phrases (e.g., "Date of birth") and detects prohibited keywords (e.g., "Guaranteed results," "Cure").
- **Sentiment Detection**: Identifies frustration, confusion, and escalation risk (e.g., threats to cancel or supervisor requests).
- **Qualification Completeness**: Checks if the agent collected all necessary patient information required for qualification.

## Technical Stack
- **Backend**: FastAPI (Python)
- **AI Orchestration**: LangGraph
- **Models**: GPT-4o / Gemini (via LangChain)
- **Task Management**: `uv`