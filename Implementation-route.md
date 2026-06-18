# AI Voice Admissions Assistant — Implementation Plan

## Overview

This README defines the staged implementation plan for the **AI Voice Admissions Assistant** feature.

The feature is a deterministic, voice-first MBA admissions intelligence system. It helps MBA/CAT aspirants understand:

- Whether their profile is competitive for target MBA institutes
- What CAT percentile range they should target
- Which colleges are realistic, stretch, or ambitious
- How specific institutes shortlist candidates
- Which profile factors are helping or hurting them

The system must use structured admissions datasets as the source of truth. LLMs should support explanation, clarification, profile extraction, and voice interaction, but must not invent admissions rules or independently calculate admissions outcomes.

---

## Core Architecture Principle

```text
Deterministic Engine = decides
LLM Agents = extract, clarify, explain, and speak
Voice Layer = makes the experience conversational
```

The system should not be implemented as a generic chatbot. It should be implemented as a deterministic admissions reasoning engine with a voice-agent wrapper.

---

## Production Data Sources

The system is expected to use the finalized production datasets:

```text
1. Admissions Methodology Database
2. Institute Factor Database
3. Profile Scoring Engine
4. Competitiveness Benchmark Database
5. Admissions Knowledge Base
```

These datasets should be treated as production source-of-truth inputs.

Do not redesign, audit, or reinterpret these datasets inside runtime logic. Runtime components should load, normalize, query, and execute against them.

---

## High-Level Runtime Flow

```text
User speaks
   ↓
Speech-to-text
   ↓
Transcript normalization
   ↓
Profile extraction
   ↓
Intent classification
   ↓
Institute/category resolution
   ↓
Profile completeness validation
   ↓
Deterministic admissions calculation
   ↓
Benchmark comparison
   ↓
Required CAT / percentile estimation
   ↓
Response plan generation
   ↓
LLM voice explanation
   ↓
Guardrail verification
   ↓
Voice output + transcript
```

---

# Implementation Stages

## Stage 0 — Data & System Foundation

### Goal

Prepare the technical base so every later feature uses the same source of truth.

### Build

Create backend repositories/loaders for:

```text
Institute master
Factor master
Profile scoring engine
Competitiveness benchmark database
Admissions knowledge base
```

Create stable identifiers for:

```text
Institute
Category
Admission cycle
Factor
Formula
Benchmark
Knowledge-base entry
```

### Components

```text
InstituteRepository
FactorRepository
ScoringRuleRepository
BenchmarkRepository
KnowledgeBaseRepository
DatasetVersionManager
```

### Example Internal APIs

```http
GET /institutes/{institute_id}/methodology
GET /institutes/{institute_id}/factors
GET /benchmarks/{institute_id}/{category}
GET /knowledge-base/{institute_id}
```

### Visible Improvement

Engineering can query institute, factor, benchmark, and knowledge-base data as clean structured JSON.

### Acceptance Criteria

- All production datasets load successfully.
- Every institute has a stable `institute_id`.
- Every benchmark is queryable by institute and category.
- Every knowledge-base response is traceable to the production dataset.
- No LLM is used in this stage.

---

## Stage 1 — Text-Based Methodology Explainer

### Goal

Build the first user-facing feature without needing full profile scoring.

### Supported Questions

```text
How does IIM Ahmedabad shortlist?
How does IIM Bangalore evaluate work experience?
Does FMS care about academics?
Which factors does IIM Calcutta use?
```

### Runtime Flow

```text
User question
   ↓
Intent detection
   ↓
Institute resolver
   ↓
Knowledge-base lookup
   ↓
LLM explanation
   ↓
Guarded answer
```

### Components

```text
IntentRouter v1
InstituteResolver v1
KnowledgeBaseRetriever v1
ExplanationAgent v1
ConfidenceAwareResponsePolicy v1
```

### Visible Improvement

The assistant can answer institute-methodology questions in simple, concise language.

### Example

```text
User: How does IIM Calcutta shortlist?

Assistant: IIM Calcutta uses CAT, Class 10, Class 12, and gender diversity in its shortlist-stage score. Graduation and work experience do not carry shortlist-stage weight in the verified production data.
```

### Acceptance Criteria

- Supports methodology explainer mode for all production institutes.
- Clearly says when exact formula or factor data is unavailable.
- Does not invent exact weights where data is low confidence or absent.
- Can answer methodology, factor, formula-summary, and caveat questions.

---

## Stage 2 — Profile Intake & Validation

### Goal

Make the assistant profile-aware.

### Supported Input

```text
My profile is 95 in 10th, 89 in 12th, 8.1 CGPA, general male engineer, 18 months work ex.
```

### Components

```text
ProfileExtractionAgent
ProfileNormalizer
ProfileCompletenessValidator
SessionProfileStore
ClarifyingQuestionGenerator
```

### Minimum User Profile Schema

```json
{
  "category": "GENERAL",
  "gender": "MALE",
  "class_10_score": 95,
  "class_12_score": 89,
  "graduation_score": 8.1,
  "graduation_score_type": "CGPA",
  "graduation_stream": "ENGINEERING",
  "work_ex_months": 18,
  "target_exam": "CAT",
  "target_percentile": null,
  "actual_percentile": null
}
```

### Visible Improvement

The assistant can extract profile details, identify missing fields, and ask relevant follow-up questions.

### Example

```text
User: Is my profile good for BLACKI?

Assistant: I can estimate that, but I need your category, gender, 10th, 12th, graduation score, academic stream, and work experience.
```

### Acceptance Criteria

- Extracts profile fields from messy natural language.
- Identifies missing profile fields.
- Stores only current-session profile unless persistent memory is explicitly introduced later.
- Does not evaluate profile until required fields are available.
- Handles partial profile gracefully.

---

## Stage 3 — Deterministic Profile Evaluation Engine

### Goal

Build the first true admissions-intelligence capability.

### Supported Questions

```text
Is my profile good for IIM Bangalore?
Is my profile good for BLACKI?
Where do I stand for IIM Ahmedabad?
```

### Components

```text
ProfileScoringEngine
CompositeScoreCalculator
FactorBreakdownGenerator
CompetitivenessClassifier v1
ResponsePlanGenerator v1
```

### Runtime Flow

```text
Profile
   ↓
Institute methodology rule
   ↓
Composite score calculation
   ↓
Factor-wise breakdown
   ↓
Competitiveness label
   ↓
Response plan
   ↓
LLM explanation
```

### Recommended Initial Institute Scope

```text
IIM Ahmedabad
IIM Bangalore
IIM Calcutta
IIM Lucknow
IIM Indore
IIM Kozhikode
FMS Delhi
MDI Gurgaon
```

### Visible Improvement

The assistant can give deterministic profile readings for selected institutes.

### Example

```text
For IIM Bangalore, your profile looks like a stretch. Your work experience helps, but the required CAT contribution remains high because Bangalore is profile-sensitive and uses academics, work experience, CAT, and gender components.
```

### Acceptance Criteria

- Same profile produces the same deterministic score output.
- Every score has a factor-level breakdown.
- Every answer includes confidence or limitation language.
- LLM does not calculate the score.
- LLM only explains the deterministic result.

---

## Stage 4 — Benchmark Comparison & Percentile Estimation

### Goal

Answer one of the highest-value user questions:

```text
What percentile should I target?
```

### Components

```text
BenchmarkComparisonEngine
RequiredCATContributionEstimator
PercentileRangeEstimator
ConfidenceLabeler
```

### Logic

```text
User profile
   ↓
Non-CAT/profile contribution
   ↓
Target institute benchmark
   ↓
Required composite gap
   ↓
Required CAT contribution
   ↓
Estimated percentile range
```

### Visible Improvement

The assistant can provide profile-aware CAT percentile target guidance.

### Example

```text
For your profile, I would not think of IIM Ahmedabad as just a percentile question. Your non-CAT profile contributes part of the composite, and CAT has to close the remaining gap. Based on the benchmark, your target should be treated as a high-percentile range, not a guaranteed cutoff.
```

### Acceptance Criteria

- Composite benchmark is the primary variable.
- Percentile is treated as a derived estimate.
- Never says “guaranteed call.”
- Returns percentile as a range, not false precision.
- Distinguishes methodology confidence from benchmark confidence.

---

## Stage 5 — College Recommendation & Gap Analysis

### Goal

Answer the third core MVP question:

```text
Which colleges are realistic for me?
```

### Components

```text
RecommendationEngine
InstituteRankingEngine
ProfileGapAnalyzer
FactorSensitivityAnalyzer
CollegeBucketGenerator
```

### Recommendation Buckets

```text
Strong
Realistic
Stretch
Ambitious
Low Probability
Insufficient Data
```

### Gap Categories

```text
Fixed gaps:
- 10th marks
- 12th marks
- Graduation marks
- Category
- Gender
- Academic stream

Partially controllable:
- Work experience, depending on timeline

Controllable:
- CAT score
- Institute targeting
- Application choices
```

### Visible Improvement

The assistant can recommend colleges and explain profile bottlenecks.

### Example

```text
Your college list should be split into realistic, stretch, and ambitious buckets. Based on your profile, CAT-heavy schools may be more forgiving than profile-heavy schools. Your biggest controllable lever is CAT, while graduation score is a fixed bottleneck.
```

### Acceptance Criteria

- Colleges are ranked by deterministic score or benchmark gap.
- LLM does not decide ranking.
- Each recommendation includes reason codes.
- Gap analysis separates fixed and improvable factors.
- Unsupported institutes are marked as insufficient data.

---

## Stage 6 — Conversation Memory & Follow-Up Handling

### Goal

Make the assistant feel like a real conversation instead of isolated Q&A.

### Components

```text
SessionMemoryManager
ConversationStateMachine
FollowUpIntentResolver
ContextCarryForwardEngine
ProfileUpdateHandler
```

### Example Flow

```text
User: My profile is 8/7/7, general male engineer, no work ex.
Assistant: Got it. Which institutes do you want me to evaluate?

User: What about IIM Indore?
Assistant: Uses existing profile + target institute = IIM Indore.

User: And Bangalore?
Assistant: Uses existing profile + target institute = IIM Bangalore.
```

### Visible Improvement

The assistant handles follow-ups without asking for the same profile again.

### Acceptance Criteria

- Session memory stores profile fields.
- User can update individual fields.
- Assistant does not re-ask known information.
- Memory is scoped to current session unless persistent memory is introduced later.
- Ambiguous follow-ups trigger clarification.

---

## Stage 7 — Voice Layer Integration

### Goal

Turn the working text-based admissions engine into a voice-first assistant.

### Components

```text
SpeechToTextService
TextToSpeechService
VoiceResponseCompressor
BargeInHandler
LatencyManager
TranscriptRenderer
VoiceSessionController
```

### Runtime Flow

```text
User speaks
   ↓
ASR
   ↓
Transcript normalization
   ↓
Existing admissions pipeline
   ↓
Short response plan
   ↓
TTS
   ↓
Transcript shown in UI
```

### Visible Improvement

The user can speak naturally and receive a spoken admissions answer.

### Example

```text
User: I am a general male engineer, 95 in 10th, 89 in 12th, 8 CGPA, 18 months work ex. Is IIM Bangalore realistic?

Assistant: For IIM Bangalore, this looks like a stretch but not out of range. Your work experience helps, but you will still need a strong CAT contribution. Treat the percentile estimate as a range, not a guarantee.
```

### Acceptance Criteria

- Spoken answers are concise.
- Text transcript is shown.
- Assistant asks one clarification at a time.
- Latency is acceptable for voice interaction.
- Voice layer does not bypass deterministic engine.

### Design Note

Do not expose long formulas in voice by default.

Use progressive disclosure:

```text
Short answer first.
Formula only if the user asks.
```

---

## Stage 8 — Guardrails, Analytics & Production Hardening

### Goal

Make the assistant safe, auditable, and reliable.

### Components

```text
ResponseGuardrailEngine
UnsupportedClaimDetector
OutOfScopeClassifier
AuditLogger
AnalyticsEventTracker
RegressionTestSuite
AdminReviewDashboard
```

### Guardrails

Block or rewrite answers containing:

```text
Guaranteed call
Guaranteed admission
Impossible claim
Unverified cutoff
CAT tutoring
Career counseling
Resume/SOP/interview advice
Open-web claims
Unsupported institute logic
```

### Analytics Events

```text
intent_detected
profile_completed
missing_field_requested
institute_queried
recommendation_generated
percentile_estimated
cannot_verify_response
out_of_scope_query
voice_latency
fallback_triggered
```

### Visible Improvement

The team can inspect system behavior, user drop-offs, common institutes, missing fields, fallback triggers, and guardrail events.

### Acceptance Criteria

- Every final answer has an audit trace.
- Every calculation includes dataset version.
- Every LLM response is checked before output.
- Regression tests pass for golden profiles.
- Out-of-scope questions are refused cleanly.

---

## Stage 9 — Full MVP Launch

### Goal

Ship the complete MVP to real users.

### MVP Includes

```text
Voice admissions Q&A
Profile intake
Profile evaluation
Methodology explanation
Percentile target guidance
Gap analysis
Target college recommendation
Institute comparison
Admissions FAQ
Confidence-aware responses
Session memory
Transcript display
Analytics
Guardrails
```

### Launch Readiness Checklist

```text
Core institutes tested
Golden profiles tested
Voice latency acceptable
Guardrails tested
Fallbacks tested
Dataset versions locked
Admin can inspect logs
Known limitations documented
```

### Visible Improvement

The product can support the core admissions assistant experience end-to-end.

---

# Suggested Repository Structure

```text
ai-voice-admissions-assistant/
  README.md
  app/
    agents/
      profile_extractor.py
      intent_router.py
      explanation_agent.py
      verifier.py
    engine/
      admissions_engine.py
      scoring_engine.py
      benchmark_engine.py
      percentile_estimator.py
      recommendation_engine.py
      gap_analysis_engine.py
    repositories/
      institute_repository.py
      factor_repository.py
      scoring_rule_repository.py
      benchmark_repository.py
      knowledge_base_repository.py
    schemas/
      profile.py
      intent.py
      institute.py
      scoring.py
      benchmark.py
      response_plan.py
    voice/
      speech_to_text.py
      text_to_speech.py
      transcript_normalizer.py
      voice_session_controller.py
    guardrails/
      response_guardrails.py
      out_of_scope.py
      unsupported_claims.py
    analytics/
      event_tracker.py
      audit_logger.py
    api/
      routes.py
      dependencies.py
  data/
    raw/
    processed/
    versions/
  tests/
    unit/
    integration/
    golden_profiles/
  docs/
    technical_prd.md
    api_contracts.md
    prompt_contracts.md
```

---

# Key API Contracts

## Profile Extraction

```http
POST /profile/extract
```

### Request

```json
{
  "transcript": "I am general male engineer, 95 in 10th, 89 in 12th, 8 CGPA, 18 months work ex."
}
```

### Response

```json
{
  "profile": {
    "category": "GENERAL",
    "gender": "MALE",
    "class_10_score": 95,
    "class_12_score": 89,
    "graduation_score": 8,
    "graduation_score_type": "CGPA",
    "graduation_stream": "ENGINEERING",
    "work_ex_months": 18
  },
  "missing_fields": []
}
```

---

## Profile Evaluation

```http
POST /admissions/evaluate-profile
```

### Request

```json
{
  "profile": {},
  "target_institutes": ["iim_bangalore", "iim_calcutta"],
  "category": "GENERAL"
}
```

### Response

```json
{
  "results": [
    {
      "institute_id": "iim_bangalore",
      "competitiveness": "STRETCH",
      "composite_score": 91.2,
      "gap_to_call": 0.1,
      "reason_codes": [
        "near_call_threshold",
        "work_experience_positive",
        "high_cat_contribution_needed"
      ]
    }
  ]
}
```

---

## Required Percentile

```http
POST /admissions/required-percentile
```

### Request

```json
{
  "profile": {},
  "target_institute": "iim_ahmedabad",
  "category": "GENERAL",
  "target_level": "CALL_THRESHOLD"
}
```

### Response

```json
{
  "institute_id": "iim_ahmedabad",
  "target_level": "CALL_THRESHOLD",
  "required_cat_contribution": 47.6,
  "estimated_percentile_range": "99.6-99.8",
  "confidence": "MEDIUM",
  "caveat": "Percentile is derived from composite benchmark and should be treated as a range."
}
```

---

# LLM Usage Boundaries

## LLMs Can Do

```text
Extract profile fields from natural language
Classify ambiguous intent
Generate clarifying questions
Convert deterministic response plans into mentor-style language
Handle voice-friendly phrasing
Summarize verified methodology text
```

## LLMs Must Not Do

```text
Invent admissions rules
Calculate composite score independently
Rank colleges independently
Estimate percentile without deterministic engine output
Present unverified information as verified
Guarantee calls or admissions
Answer out-of-scope CAT tutoring or career counseling questions
```

---

# Response Plan Contract

The deterministic engine should generate a response plan before the explanation agent speaks.

```json
{
  "response_type": "PROFILE_EVALUATION",
  "direct_answer": "Your profile looks like a stretch for IIM Bangalore.",
  "facts": [
    {
      "label": "Competitiveness",
      "value": "STRETCH"
    },
    {
      "label": "Main positive factor",
      "value": "Work experience"
    },
    {
      "label": "Main pressure factor",
      "value": "High CAT contribution needed"
    }
  ],
  "required_caveats": [
    "Percentile estimates are ranges, not guarantees."
  ],
  "forbidden_claims": [
    "guaranteed call",
    "guaranteed admission",
    "impossible"
  ]
}
```

The explanation agent should only verbalize this object. It should not introduce new admissions facts.

---

# Testing Strategy

## Golden Profile Test Set

Create deterministic test cases for:

```text
Strong academics, no work experience
Weak academics, high CAT target
Average academics, strong work experience
General male engineer
Non-engineer female
Reserved category candidate
Low graduation score
High 10th and low 12th
Post-CAT actual percentile user
```

## Expected Output Per Test

```text
Composite score
Factor breakdown
Competitiveness label
Benchmark gap
Required CAT contribution
Estimated percentile range
Reason codes
Confidence label
Caveats
```

## Regression Rule

Any change to these should trigger review:

```text
Dataset version
Formula logic
Benchmark logic
Prompt template
LLM model
Response planner
Guardrail rule
```

---

# Final Development Strategy

Build in this order:

```text
Backend intelligence first
Text-based assistant second
Voice interface third
Production hardening last
```

Do not build in this order:

```text
Voice UI first
Generic LLM chatbot second
Admissions logic later
```

The correct progression is:

```text
Stage 1: It knows verified facts.
Stage 2: It understands the user profile.
Stage 3: It calculates profile fit.
Stage 4: It estimates CAT target.
Stage 5: It recommends colleges.
Stage 6: It holds a conversation.
Stage 7: It speaks naturally.
Stage 8: It becomes safe and production-ready.
```

This ensures every stage produces visible improvement while preserving the deterministic admissions engine as the core product advantage.

