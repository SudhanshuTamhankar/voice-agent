# Voice CLI Stress Test Report
This report contains the raw text output from the `AskResponse` API, simulating the exact transcripts processed by the CLI `voice_chat.py`.

## Test Case 1: FAQ & Methodology
**Description:** Asking about FMS Delhi shortlist criteria

> **User Speech:** 'how does FMS Delhi shortlist candidates for interview'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> FMS Delhi determines its shortlist and final selection through a structured weighted process. Here is how they handle the evaluation:

**Shortlisting Criteria**
For the initial interview shortlist, FMS Delhi uses a weighted score based on your CAT performance. The formula is: **(0.40 × VARC) + (0.30 × DILR) + (0.30 × QA)**. Additionally, female candidates receive a bonus of 5 points at this stage. Please note that these CAT section values represent weights rather than sectional minimum cutoffs.

**Final Selection Matrix**
Once candidates are selected for the interview, the final admission decision is based on a broader matrix:
*   **50%:** CAT score
*   **10%:** Class X marks
*   **10%:** Class XII marks
*   **10%:** Statement of Purpose (SOP) discussion
*   **5%:** Extempore
*   **15%:** Personal Interview (PI)

Finally, women receive an additional 5-point bonus at the interview stage of the final selection process.

---

## Test Case 2: FAQ & Methodology
**Description:** Asking about IIM Ahmedabad criteria

> **User Speech:** 'what is the selection criteria for IIM Ahmedabad'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> IIM Ahmedabad selects candidates through a two-stage process: the initial shortlisting for interviews and the final selection matrix.

**Initial Shortlisting Criteria**
For the domestic route, the institute uses a composite score based on your CAT performance and an Academic Rating (AR). 
*   **CAT Cutoffs:** For the General/EWS category, you must achieve a minimum of 95 overall and 85 in each section. (Cutoffs for other categories and PwD are published separately).
*   **Academic Rating (AR):** This is calculated as the sum of components A+B+C+D+E. This calculation considers your academic history, including stream-wise thresholds and 80th-percentile bachelor thresholds.
*   **Composite Score (CS) Formula:** Your initial shortlist position is determined by: CS = 0.35 × (AR/38) + 0.65 × (CAT/204).
*   **Other Factors:** The calculation also accounts for work experience—calculated as 0.20 × (months−11), capped at 5 points—and gender diversity, where male candidates receive 0 points and all others receive 3 points.

For international applicants, IIM Ahmedabad provides a separate route using GMAT or GMAT Focus scores (minimum 720 for previous GMAT or 665 for GMAT Focus), with specific sectional minima applied.

**Final Selection Matrix**
Please note that regarding the specific weights or formula used for the final selection matrix post-interview, there is a lack of verified published data.

---

## Test Case 3: College Recommendation (Multi-turn)
**Description:** Asking for college recommendations with a 999 profile and 24 months work ex, then giving percentile

> **User Speech:** 'which colleges should I apply to?'
> **🤖 Assistant [Intent: COLLEGE_RECOMMENDATION]:**
> I can't create a reliable college recommendation list without some CAT estimate, because the same profile can lead to very different college options at different percentiles. You can share your expected percentile, current mock percentile, or even a rough target range, and I'll use that to build the recommendation buckets.

> **User Speech:** 'I have a 999 profile general male with 24 months of work experience'
> **🤖 Assistant [Intent: COLLEGE_RECOMMENDATION]:**
> I can't create a reliable college recommendation list without some CAT estimate, because the same profile can lead to very different college options at different percentiles. You can share your expected percentile, current mock percentile, or even a rough target range, and I'll use that to build the recommendation buckets.

> **User Speech:** 'my cat score is 99.56 percentile'
> **🤖 Assistant [Intent: COLLEGE_RECOMMENDATION]:**
> I'm sorry, I cannot provide a definitive or guaranteed prediction about that. I can only provide mathematical estimates based on historical composite formulas. Let's focus on your target percentile or evaluating your current profile strength.

---

## Test Case 4: Profile Evaluation (Multi-turn)
**Description:** Asking for profile evaluation for IIM Indore

> **User Speech:** 'can you evaluate my chances for IIM Indore?'
> **🤖 Assistant [Intent: UNKNOWN]:**
> 

> **User Speech:** 'I got 85 in 10th 88 in 12th and 82 in graduation. I am an engineer fresher.'
> **🤖 Assistant [Intent: UNKNOWN]:**
> 

> **User Speech:** 'my cat percentile is 98'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> That is a great CAT percentile to start with! To give you an accurate assessment for the top IIMs, could you please share your category, gender, Class 10 and 12 percentages, graduation score and stream, and your total work experience in months?

---

## Test Case 5: Target Percentile
**Description:** Asking for target percentile for IIM Calcutta with partial profile

> **User Speech:** 'what percentile do I need for IIM Calcutta?'
> **🤖 Assistant [Intent: TARGET_PERCENTILE]:**
> IIM Calcutta is a dream school, and to give you a precise target percentile calculation, I need a bit more context about your background. Could you please share your Category, Gender, Class 10/12/Graduation percentages, Graduation stream, and total months of work experience so I can run the numbers for you?

> **User Speech:** 'I am a general female with 90 in 10th and 95 in 12th and 85 in graduation. 0 work experience.'
> **🤖 Assistant [Intent: TARGET_PERCENTILE]:**
> That is an excellent academic profile to start with, and I've noted down your scores and lack of work experience. To help me run a precise calculation for your target of IIM Calcutta, could you please let me know your graduation stream (e.g., Engineering, Commerce, Arts, etc.)?

---

## Test Case 6: Edge Case - Impossible Profile
**Description:** Asking for target percentile at IIM Bangalore with a 60/60/60 profile

> **User Speech:** 'what percentile do I need for IIM Bangalore?'
> **🤖 Assistant [Intent: TARGET_PERCENTILE]:**
> To give you an accurate estimate of the percentile you'll need for IIM Bangalore, I first need to gather a few more details about your academic and professional background.

I have noted your goal for IIM Bangalore, but to run the calculation, could you please share your category, gender, Class 10 and 12 marks, graduation stream and score, and your total work experience in months?

> **User Speech:** 'I am a general male engineer. I scored 60 in 10th, 60 in 12th, and 60 in graduation. fresher.'
> **🤖 Assistant [Intent: UNKNOWN]:**
> 

---

## Test Case 7: Out of Domain - General
**Description:** Asking a completely unrelated question

> **User Speech:** 'what is the capital of France?'
> **🤖 Assistant [Intent: UNKNOWN]:**
> 

---

## Test Case 8: Out of Domain - Clymber
**Description:** Asking about CAT preparation strategy

> **User Speech:** 'can you give me a study plan for DILR?'
> **🤖 Assistant [Intent: UNKNOWN]:**
> 

---
