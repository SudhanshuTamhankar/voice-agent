**PRODUCT REQUIREMENTS DOCUMENT**

**AI Voice Admissions Assistant**

_Voice-first MBA admissions intelligence for CAT aspirants_

Prepared by Sudhanshu

| **Product Mode**   | Voice-first admissions assistant          |
| ------------------ | ----------------------------------------- |
| **Primary User**   | MBA/CAT aspirant                          |
| **Primary Source** | Verified admissions intelligence database |

# 1\. Executive Summary

The AI Voice Admissions Assistant is a voice-first product that helps MBA aspirants understand profile-based admissions decisions for top Indian B-schools.

The assistant converts Clymber's verified admissions intelligence database into a user-facing experience where students can ask questions naturally and receive concise, institute-specific, evidence-grounded guidance.

The product is not a general chatbot, CAT tutor, career counselor, or search engine. It is a constrained admissions mentor focused on:

- Profile evaluation
- Percentile targeting
- Stage-1 shortlisting logic
- Institute comparison
- College targeting
- Admissions strategy

The core product promise:

**"Ask naturally. Understand where you stand. Get verified, institute-specific admissions guidance without relying on rumours."**

The MVP should help aspirants answer three high-value questions:

1\. "Is my profile good enough?"

2\. "What percentile should I target?"

3\. "Which colleges are realistic for me?"

The assistant should use structured verified admissions data as the source of truth. The AI layer should explain, clarify, and personalize, but not invent admission rules.

# 2\. Problem Statement

MBA aspirants understand CAT percentiles, but they do not understand how institutes evaluate profiles.

Most students know that a higher CAT percentile helps. What they do not know is:

- Whether their 10th, 12th, or graduation marks are a bottleneck
- Whether work experience helps them
- Whether diversity factors matter for them
- Which institutes are CAT-heavy versus profile-heavy
- Why two students with similar CAT percentiles may receive different calls
- Which colleges are realistic for their profile
- What they should improve before CAT or applications

Current information sources are fragmented and unreliable:

- YouTube videos
- Telegram groups
- Reddit threads
- Quora answers
- Coaching discussions
- Peer advice
- Outdated admission PDFs

This creates anxiety and poor decision-making. Students either overestimate their chances, underestimate themselves, or apply without understanding institute fit.

The product solves this by giving aspirants a trusted voice assistant that explains admissions logic in simple, personalized language.

# 3\. Target Users

## Primary Users

CAT aspirants applying to Indian MBA programs

These users are preparing for CAT and want to understand how their profile affects admissions.

## Key Segments

| **Segment**              | **Description**                                                | **Primary Need**                    |
| ------------------------ | -------------------------------------------------------------- | ----------------------------------- |
| First-time CAT aspirants | Early-stage aspirants who do not understand profile evaluation | Profile clarity                     |
| Final-year students      | Students with fixed academics and no work experience           | Realistic college targeting         |
| Working professionals    | Aspirants with 12-48 months of experience                      | Work-experience impact              |
| Repeat takers            | Aspirants deciding whether to reattempt CAT                    | Gap and improvement analysis        |
| Non-engineers            | Commerce, arts, science, humanities students                   | Diversity and fit analysis          |
| Profile-anxious students | Students worried about low 10th, 12th, or graduation scores    | Bottleneck diagnosis                |
| Post-result users        | Students with actual CAT percentile                            | Call probability and target mapping |

## Secondary Users

- Admissions mentors
- Clymber counselors
- Product teams building profile tools
- Business teams designing admissions-focused campaigns

# 4\. Product Vision

Build India's most trusted voice-first MBA admissions intelligence assistant.

The assistant should feel like an experienced admissions mentor who understands verified institute rules and can explain them clearly in spoken language.

The product should help users move from:

Confusion → Clarity → Targeting → Action

The product should not overwhelm users with policy details. Instead, it should simplify admissions logic into actionable guidance.

## Product Principles

1\. **Verified over viral**

Use the verified admissions database as the primary source of truth.

2\. **Voice-first, not text-first**

Responses should be short, conversational, and easy to understand when spoken.

3\. **Ask before assuming**

If profile information is missing, the assistant should ask clarifying questions.

4\. **Explain the why**

Every recommendation should include a simple reason.

5\. **Do not fabricate**

If an institute does not publish a verified rule, the assistant should say so.

6\. **Admissions-only scope**

The assistant should not drift into CAT tutoring, resume review, or career counseling.

# 5\. Key User Journeys

## Journey 1 - Quick Profile Evaluation

**User goal:** "Is my profile good enough?"

Flow:

1\. User asks about profile strength.

2\. Assistant asks for missing profile fields.

3\. User provides academics, category, gender, stream, work experience, and target exam score if available.

4\. Assistant evaluates profile against verified admissions factors.

5\. Assistant gives concise profile reading.

Expected outcome:

User understands profile strengths, weaknesses, and likely bottlenecks.

## Journey 2 - Percentile Target Planning

**User goal:** "What CAT percentile should I target?"

Flow:

1\. User asks for target percentile.

2\. Assistant identifies target institute or asks for target college list.

3\. Assistant uses profile and institute methodology.

4\. Assistant gives target guidance with reasoning.

5\. Assistant explains which profile factors increase or reduce pressure on CAT score.

Expected outcome:

User gets a practical CAT target aligned to their profile and preferred institutes.

## Journey 3 - Institute Methodology Explanation

**User goal:** "How does this college shortlist?"

Flow:

1\. User names an institute.

2\. Assistant retrieves verified Stage-1 methodology.

3\. Assistant explains major factors in simple language.

4\. Assistant offers formula details only if the user asks.

Expected outcome:

User understands how the institute evaluates candidates without reading policy documents.

## Journey 4 - Profile Gap Analysis

**User goal:** "What is hurting my profile?"

Flow:

1\. User shares profile or asks for diagnosis.

2\. Assistant identifies weak components.

3\. Assistant distinguishes fixed factors from improvable factors.

4\. Assistant gives next-step guidance.

Expected outcome:

User knows what is hurting them and what they can still improve.

## Journey 5 - Target College Recommendation

**User goal:** "Which colleges should I target?"

Flow:

1\. User provides profile and current/target percentile.

2\. Assistant compares profile against verified institute methodologies.

3\. Assistant groups colleges into realistic, stretch, and lower-fit targets.

4\. Assistant explains why each group fits.

Expected outcome:

User receives an application strategy instead of a generic college list.

## Journey 6 - Institute Comparison

**User goal:** "Which colleges value work experience more?"

Flow:

1\. User asks comparative question.

2\. Assistant identifies relevant factor.

3\. Assistant compares institutes using verified methodology.

4\. Assistant summarizes in concise spoken form.

Expected outcome:

User understands institute differences clearly.

# 6\. Core Features

## Feature 1 - Voice Profile Evaluator

User Problem Solved

Students do not know whether their profile is strong, average, or risky for MBA admissions.

Description

The assistant evaluates a user's profile using verified admissions factors such as academics, category, gender, academic background, work experience, and target score.

Inputs Required

- 10th marks
- 12th marks
- Graduation marks
- Academic stream
- Gender
- Category
- Work experience
- Target exam and expected percentile

Expected Output

- Concise profile assessment
- Strengths
- Weaknesses
- Institute-fit direction
- Missing information if required

Success Criteria

- User completes profile input without confusion
- User understands at least one strength and one risk factor
- User receives clear next-step guidance

## Feature 2 - Institute Shortlisting Explainer

User Problem Solved

Students do not understand how individual institutes shortlist candidates.

Description

The assistant explains verified Stage-1 shortlisting methodology for a selected institute in simple spoken language.

Inputs Required

- Institute name
- Optional: user profile for personalized explanation

Expected Output

- Shortlisting methodology summary
- Key factors used
- Published formula or weightage if available
- Important caveats if exact methodology is unavailable

Success Criteria

- User understands how the institute evaluates candidates
- Assistant does not expose unverified rules as verified
- User can ask follow-up questions naturally

## Feature 3 - CAT Percentile Target Planner

User Problem Solved

Students do not know what percentile they should realistically target based on their profile.

Description

The assistant gives institute-specific percentile guidance using verified shortlisting logic and profile factors.

Inputs Required

- Target institute or institute group
- User profile
- Category
- Current mock score or target score
- Exam year/cycle if relevant

Expected Output

- Target percentile guidance
- Explanation of profile pressure
- Schools where the target is realistic or insufficient

Success Criteria

- User receives actionable percentile direction
- Assistant explains why the target changes by institute
- No unsupported call guarantee is given

## Feature 4 - Profile Gap Analyzer

User Problem Solved

Students know something is weak but do not know what specifically affects admissions.

Description

The assistant identifies which profile factors are limiting the user's chances for selected institutes.

Inputs Required

- Complete or partial profile
- Target institutes
- Current or expected percentile

Expected Output

- Bottleneck factors
- Fixed factors versus improvable factors
- Actionable improvement focus

Success Criteria

- User understands what is hurting their profile
- User gets practical next steps
- Assistant avoids vague motivation-style advice

## Feature 5 - Target College Recommender

User Problem Solved

Students struggle to build a realistic MBA college list.

Description

The assistant recommends colleges based on verified shortlisting methodologies and user profile fit.

Inputs Required

- Profile
- Expected percentile
- Category
- Preferred college type
- Optional: location, fees, exam preference

Expected Output

- Realistic targets
- Stretch targets
- Lower-fit institutes
- Reasoning for each group

Success Criteria

- User saves or accepts a target list
- Recommendations are explainable
- No college is recommended using unsupported methodology

## Feature 6 - Institute Comparison Assistant

User Problem Solved

Students do not know how institutes differ in academics, work experience, diversity, and CAT dependence.

Description

The assistant compares institutes based on verified factors.

Inputs Required

- Two or more institute names
- Comparison factor, if specified

Expected Output

- Concise comparison
- Factor-level differences
- Recommendation based on user profile, if available

Success Criteria

- User understands differences within one voice response
- Numerical values are preserved where available
- Assistant does not overgeneralize

## Feature 7 - Admissions FAQ Resolver

User Problem Solved

Students repeatedly ask common admissions questions and receive inconsistent answers from informal sources.

Description

The assistant answers common admissions FAQs within product scope.

Inputs Required

- User question
- Optional: profile context

Expected Output

- Direct answer
- Institute-specific caveat if needed
- Follow-up prompt where profile context matters

Success Criteria

- User receives answer in under 30 seconds
- Assistant stays within MBA admissions scope
- User is guided to profile-based evaluation when needed

## Feature 8 - Confidence-Aware Answering

User Problem Solved

Students cannot distinguish verified admissions rules from rumours.

Description

The assistant classifies answers into verified, partially available, or unavailable based on database confidence.

Inputs Required

- Institute
- Factor or methodology question

Expected Output

- Verified answer where available
- Cautionary answer where data is incomplete
- Refusal to fabricate when methodology is unavailable

Success Criteria

- No unverified value is presented as verified
- Users trust uncertainty instead of receiving false precision
- Assistant maintains credibility

# 7\. Flow Chart: How It Works Across Layers

User speaks question  
↓  
Voice Input Layer  
Converts speech to text  
↓  
Conversation Manager  
Understands intent and checks missing profile fields  
↓  
Intent Classification  
Profile evaluation / percentile target / institute method / comparison / FAQ  
↓  
Profile Context Layer  
Uses current-session profile information only  
↓  
Admissions Logic Engine(Completely Deterministically Designed)  
Runs deterministic rules where verified formulas exist  
↓  
Verified Admissions Database(Extensively Researched upon)  
Stage-1 factors, formulas, weightages, confidence levels, source metadata  
↓  
Response Policy Layer  
Decides: exact answer / guarded answer / cannot verify  
↓  
LLM Explanation Layer  
Converts structured output into concise mentor-style language  
↓  
Voice Output Layer  
Speaks the final response  
↓  
Follow-up Prompt  
Asks for missing information or suggests next useful action

## Response Modes

| **Mode**       | **When Used**                                        | **Product Behavior**                                           |
| -------------- | ---------------------------------------------------- | -------------------------------------------------------------- |
| Exact Answer   | Verified formula or factor exists                    | Give direct answer with concise explanation                    |
| Guarded Answer | Broad rule is verified but exact value is incomplete | Explain what is known and what is not                          |
| Cannot Verify  | Rule is unsupported or conflict-marked               | Do not fabricate; ask user to proceed with verified facts only |

# 8\. MVP Scope

## In Scope

The MVP should include:

1\. Voice-based admissions Q&A

2\. User profile intake

3\. Profile strength evaluation

4\. Institute shortlisting methodology explanation

5\. CAT percentile target guidance

6\. Profile gap analysis

7\. Target college recommendation

8\. Institute comparison

9\. Admissions FAQ handling

10\. Confidence-aware responses

11\. Current-session memory

12\. Text transcript of spoken response

## Out of Scope

The MVP should not include:

- CAT Quant tutoring
- CAT VARC tutoring
- CAT DILR tutoring
- Resume review
- SOP writing
- Interview preparation
- Current affairs
- Career counseling
- Placement guidance
- Open-web search answers
- Unverified call prediction
- Guaranteed admission probability
- General non-profile-based questions unrelated to MBA admissions methodology
- Overall score-based predictions or recommendations without profile context

## MVP Behavior Standards

The assistant should:

- Ask for missing information before recommending colleges
- Keep spoken responses concise
- Explain reasoning simply
- Avoid unsupported claims
- Stay focused on MBA admissions
- Use verified database logic for admissions calculations
- Say when exact methodology is unavailable

# 9\. Competitive Differentiation

## Current Alternatives

Students currently rely on:

- Predictor tools
- Coaching mentors
- YouTube videos
- Telegram groups
- Reddit and Quora
- Static admission PDFs
- Peer advice

## Product Differentiators

| **Differentiator**           | **Why It Matters**                           |
| ---------------------------- | -------------------------------------------- |
| Verified admissions database | Reduces dependency on rumours                |
| Voice-first interface        | Easier for stressed aspirants to use quickly |
| Institute-specific logic     | Avoids generic admissions advice             |
| Profile-aware guidance       | Makes answers personal                       |
| Confidence-aware answering   | Prevents hallucinated admissions claims      |
| Deterministic logic layer    | Makes calculations more reliable             |
| Mentor-style explanation     | Makes complex rules understandable           |
| Constrained scope            | Improves trust and product clarity           |

## Positioning Statement

The AI Voice Admissions Assistant is not a chatbot. It is a verified admissions mentor that helps MBA aspirants understand where they stand, what percentile they need, and which colleges are realistic for their profile.

# 10\. Example User Interactions

## Interaction 1 - Profile Evaluation

User:

"My profile is 8/7/7, general male engineer, no work experience. Is it good enough?"

Assistant:

"Your profile is workable, but it may be challenging for institutes that place weight on academics and diversity. Your CAT score will need to do more heavy lifting. Tell me your target colleges, and I'll help you identify which ones are more realistic."

## Interaction 2 - Institute Methodology

User:

"How does IIM Bangalore shortlist?"

Assistant:

"IIM Bangalore uses a profile-sensitive pre-interview process. It considers CAT, school academics, graduation, work experience or professional qualification, and gender diversity. If you share your profile, I can explain how this methodology affects you specifically."

## Interaction 3 - Percentile Target

User:

"What percentile should I target for FMS?"

Assistant:

"FMS is highly CAT-driven at the shortlist stage. Your CAT score matters much more than most profile factors. Share your category and target score range, and I can give you a more useful target estimate."

## Interaction 4 - Gap Analysis

User:

"What is hurting my profile the most?"

Assistant:

"Based on what you shared, your weakest factor is graduation score. Your 10th and 12th are acceptable, but for profile-heavy institutes, graduation may reduce your shortlist strength. Your best lever now is maximizing CAT percentile and targeting institutes where CAT carries more weight."

## Interaction 5 - College Targeting

User:

"Which colleges should I target if I get around 97 percentile?"

Assistant:

"I'll need your profile first because 97 percentile means different things for different candidates. Tell me your 10th, 12th, graduation, category, gender, academic background, and work experience."

## Interaction 6 - Boundary Handling

User:

"Can you teach me DILR?"

Assistant:

"I can't teach DILR here. This assistant is focused on MBA admissions and profile-based college targeting. I can help you understand what percentile you may need and which colleges fit your profile."

# 11\. Most Common Aspirant Questions

1\. Is my profile good enough for top IIMs?

2\. What CAT percentile should I target with my profile?

3\. Can weak academics be compensated by a high CAT score?

4\. Which colleges value work experience?

5\. Which colleges care less about graduation marks?

6\. Does being a non-engineer help in MBA admissions?

7\. How does IIM Ahmedabad shortlist candidates?

8\. Why did someone with a lower percentile get a call while I did not?

9\. Which colleges are realistic for my profile?

10\. What should I improve before CAT and applications?

# 12\. Work Completed Till Now

## Admissions Database Creation

A verified admissions intelligence database has already been created for major Indian B-schools.

The database includes:

- Stage-1 shortlisting factors
- Academic evaluation criteria
- Work-experience evaluation criteria
- Diversity factors
- Professional qualification rules
- Institute-specific formulas
- Published weightages
- Admission-cycle details
- Source references
- Confidence ratings

## Verification Work Completed

The admissions intelligence has gone through multi-stage verification.

Completed work includes:

- Source discovery
- Extraction of admission methodologies
- Stage-3 verification audits
- Conflict detection
- Confidence classification
- Factor-level reconciliation
- Final database consolidation
- Engineering-ready dataset generation

## Current Readiness

The product is ready to move from research and data preparation into productization.

The next phase should focus on:

- Voice UX
- Intent taxonomy
- Profile intake flow
- Response templates
- Admissions logic integration
- MVP prototyping
- User testing