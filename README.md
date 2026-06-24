# Clymber AI Admissions Assistant

Clymber AI Admissions Assistant is a specialized Voice-first Agent designed to help MBA aspirants navigate the complex admission processes of top Indian Business Schools (IIMs, FMS, XLRI, etc.). It calculates deterministic composite scores, estimates target percentiles, and provides college recommendations based on real historical data—delivered through an interactive, LLM-powered voice UI.

## 🚀 Features

- **End-to-End Voice UX:** A polished, PPT-style "Smart Card" UI. The agent speaks the nuanced explanations aloud (via Edge-TTS) while displaying clean, readable summaries (Score Breakdowns, Methodologies, Target Percentiles) in the widget.
- **Deterministic Evaluation Engine:** Calculates actual composite scores mathematically using exact formulas from IIM admissions criteria (e.g., IIM Ahmedabad, Bangalore, Calcutta, Lucknow, Kozhikode, Indore, FMS).
- **Intelligent Prompting:** Powered by a semantic parser and multi-agent architecture via `Groq Llama-3-70b-8192`. The system intelligently handles intent routing (Methodology, Profile Evaluation, Target Percentile, College Recommendation).
- **Guardrails:** Prevents out-of-domain interactions and gently deflects test prep queries to the main Clymber platform.
- **Frontend Integration:** Seamlessly injects as a floating widget into any static HTML landing page, featuring a synchronized TTS-and-Visual interaction flow.

## 🛠️ Tech Stack

- **Backend:** FastAPI, Python 3.12
- **LLM Engine:** Groq API (`llama3-70b-8192`) for near-zero latency intent classification and response generation.
- **Voice / Audio:** Web Speech API for transcription, Microsoft Edge-TTS for high-quality voice synthesis.
- **Frontend:** Vanilla HTML/CSS/JS (Widget), communicating asynchronously with the FastAPI backend.

## ⚙️ Architecture

The backend utilizes a sophisticated multi-agent pipeline to ensure mathematical accuracy while maintaining conversational fluidity:
1. **Semantic Parser:** Identifies the user's core intent (`PROFILE_EVALUATION`, `TARGET_PERCENTILE`, `METHODOLOGY`, etc.) and the target institute.
2. **Profile Extraction Agent:** Persists and updates user parameters (Academics, Work Ex, Category) across the session.
3. **Deterministic Math Engines:** `ProfileScoringEngine` and `PercentileEstimatorService` execute hard-coded admissions algorithms against benchmark data.
4. **Verbalization Agents:** (`EvaluationAgent`, `TargetPercentileAgent`, `ExplanationAgent`) translate the raw mathematical data into a conversational script and generate a structured `visual_payload` for the UI.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A Groq API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SudhanshuTamhankar/voice-agent.git
   cd voice-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup:**
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the Application:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Interact:**
   Open your browser and navigate to `http://localhost:8000`. Click the floating purple microphone icon to start speaking to the Admissions Assistant!

## 📝 License

Proprietary Software - Clymber. All rights reserved.
