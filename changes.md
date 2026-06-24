# Voice Agent Implementation Analysis & Proposed Changes

Based on the deep stress test analysis of the Voice Agent across the 30 defined scenarios, several critical implementation lags and logical faults were identified. 

Here is a detailed breakdown of the outputs that did not align with expectations and the changes needed to correct them.

---

## 1. Failure to Process Multiple Institutes (Scenario 30)

**The Fault**: When a user asks about multiple colleges in a single query (e.g., *"Can I get into SPJIMR or XLRI?"*), the agent only acknowledges one of them and completely ignores the other.
**The Cause**: In `app/services/semantic_parser.py`, the `ParserOutput` schema defines `institute_id` as a single `Optional[str]`. The LLM is forced to pick only one institute from the user's query and discard the rest.
**Proposed Change**: 
- Update the `ParserOutput` in `semantic_parser.py` to use a list: `institute_ids: list[str]`.
- Update the parsing prompt to instruct the LLM to extract an array of all mentioned institutes.
- Modify `routes.py` to iterate over the `institute_ids` array and append the results (Evaluation, Target Percentile, or Methodology) for all requested colleges into a unified response.

---

## 2. "BLACKI" Alias Parsing Failure (Scenario 27)

**The Fault**: When a user says *"Evaluate my profile for blacki"*, the agent responds with an out-of-context prompt: *"Which institute would you like me to evaluate your chances for?"*
**The Cause**: The `valid_institutes` list passed to the `SemanticParser` in `routes.py` is generated directly from the database (`institute_repo.get_all()`). Since "blacki" is an alias and not an official DB entity, the LLM parser maps it to `null`. Without an `institute_id`, `routes.py` falls back to asking the user to specify an institute, effectively ignoring the explicit request for BLACKI.
**Proposed Change**:
- In `routes.py`, dynamically append common aliases like `"blacki"` to the `valid_institute_ids` list before instantiating the `SemanticParser`.
- Add an explicit instruction in the parser prompt that "blacki" maps to the string literal `"blacki"`.

---

## 3. "BLACKI" Target Percentile Benchmark Crash (Scenario 28)

**The Fault**: If the user asks *"What percentile should I target for blacki?"* and the parser manages to pass `"blacki"` as the `institute_id`, the agent responds with: *"No benchmark data available for this institute."*
**The Cause**: The `TARGET_PERCENTILE` intent block in `routes.py` directly calls `percentile_estimator.estimate_target(profile, institute_id)`. The estimator queries the `BenchmarkRepository` for the ID `"blacki"`. Because benchmarks only exist for individual institutes (e.g., `iim_ahmedabad`), the lookup fails immediately.
**Proposed Change**: 
- In `routes.py` under the `TARGET_PERCENTILE` flow, intercept `"blacki"` and expand it to the constituent IIMs (Ahmedabad, Bangalore, Calcutta, Lucknow, Kozhikode, Indore).
- Loop over this list, call `estimate_target` for each individual institute, and aggregate the results before passing them to the `TargetPercentileAgent` for formatting.

---

## 4. Brittle Context Restoration Heuristics

**The Fault**: The agent occasionally gets confused when a user provides partial information across multiple turns, especially switching between intents without explicitly restating the college name.
**The Cause**: In `routes.py`, context restoration relies on hardcoded `if-else` blocks (e.g., `if intent == "TARGET_PERCENTILE" and profile.last_intent == "COLLEGE_RECOMMENDATION"...`). This makes assumptions about parsing errors that are not deterministic.
**Proposed Change**:
- Move the state management directly into the LLM logic by providing the conversation history to the `SemanticParser`.
- Allow the parser to output context-aware intents rather than relying on brittle rule-based overwrites in the API layer.

---

## 5. Lack of Resilience Against API Limits

**The Fault**: The agent fails ungracefully when the backend LLM service hits rate limits (like Gemini's 15 RPM or GitHub Models' 50 RPD), resulting in HTTP 500 errors.
**The Cause**: `LLMService` lacks built-in retry mechanisms and `routes.py` throws an unhandled `HTTPException` when `generate_text` or `generate_json` fails.
**Proposed Change**:
- Implement exponential backoff using the `tenacity` library inside `LLMService` to retry requests on `429` (Rate Limit) errors.
- Add fallback conversational responses in `routes.py` to politely inform the user if the service is temporarily overloaded, rather than breaking the application flow.

---

## 6. "Graduation Stream" Extraction Loop (Scenarios 9-22)

**The Fault**: In almost all profile evaluation and target percentile queries (Scenarios 9 through 22), the agent gets stuck repeatedly asking the user for their "Graduation Stream", even if the user provides terms like "Engineer", "Fresher", or implicit context.
**The Cause**: The `SemanticParser` requires an explicit match for the `graduation_stream` field (e.g., "Engineering", "Arts", "Science"). If the user says "Engineer" instead of "Engineering", or doesn't provide it, the parser outputs `null` for `graduation_stream`. `routes.py` considers the profile incomplete and forces the conversational agent to ask for it, creating an infinite loop.
**Proposed Change**:
- Update `semantic_parser.py` to instruct the LLM to aggressively infer the stream (e.g., map "Engineer" -> "Engineering", "BSc" -> "Science").
- Make `graduation_stream` strictly **optional** in `routes.py`. If missing, default it to "Engineering" (the most common pool) for the sake of percentile estimation, or allow the calculation to proceed without it rather than hard-blocking the user.
