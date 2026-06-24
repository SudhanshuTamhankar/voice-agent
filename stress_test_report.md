# Automated Stress Test Report
**Date:** June 19, 2026
**Target:** AI Voice Admissions Assistant

This report details the exact behavior, intent classification, and full text responses of the assistant when subjected to the stress test scenarios.

---

### Category 1: Messy Profile Dump
**Objective:** Test if the system can handle messy, out-of-order, or unusual profile inputs.

* **User Prompt:** "I am an OBC non-creamy layer female from an arts background. I scored 8.2 CGPA in 10th, 84 percent in 12th, and my graduation score is 71 percent. I have been working for 42 months and I expect a 98 percentile in CAT. Evaluate me for IIM Calcutta."
* **Intent Classified:** `PROFILE_EVALUATION`
* **Institute Identified:** `iim_calcutta`
* **Full Assistant Output:**
> For IIM Calcutta, your profile is Need More Information.
> 
> The main reason is that IIM Calcutta's shortlisting process relies on a proprietary composite score formula that weighs your past academic performance, CAT percentile, and diversity factors against the competitive pool of applicants for that specific cycle. While your credentials provide a solid foundation, the final outcome depends on how these variables interact with the evolving annual cut-offs and the scores of other candidates in your category.
> 
> Your strongest factors are your expected 98 percentile in the CAT, which is a significant academic indicator, alongside your 42 months of relevant work experience and your diversity profile as an OBC non-creamy layer female candidate, which is viewed positively in the selection process.
> 
> The main pressure points are the volatility of the selection criteria for IIM Calcutta, where the high weightage given to 10th and 12th board marks can influence your composite score, and the fact that final benchmarks are relative to the overall performance of the applicant pool.
> 
> The next step is to finalize your CAT score, monitor the official IIM Calcutta admission policy document for the current cycle to understand the specific weightage distribution, and prepare thoroughly for the subsequent interview rounds if shortlisted.
> 
> This is based on composite-score evaluation, so treat it as guidance, not a guaranteed call prediction.

---

### Category 2: Impossible Gap
**Objective:** Test if the math engine correctly identifies impossible gaps without insulting the user, and if the guardrail allows the mathematically impossible truth.

* **User Prompt:** "I am a general male engineer. 60% in 10th, 65% in 12th, 60% in graduation. 0 work experience. What CAT percentile do I need for IIM Bangalore?"
* **Intent Classified:** `TARGET_PERCENTILE`
* **Institute Identified:** `iim_bangalore`
* **Full Assistant Output:**
> Hello. As your MBA Admissions Assistant, I have carefully analyzed your profile against the selection criteria for IIM Bangalore.
> 
> I must be transparent with you regarding your prospects at this specific institute. IIM Bangalore utilizes a very rigorous Composite Score formula that heavily weights academic consistency across Class 10, Class 12, and your Graduation.
> 
> Based on the current weightage system, your academic profile (60/65/60) poses a significant challenge. Even with a perfect 100 percentile in the CAT, the mathematical constraints of the IIM Bangalore selection model make it impossible to reach the required threshold for a final call. I understand this is difficult news to hear, and I want to be as factual as possible to help you focus your efforts where they will yield the best results.
> 
> **My recommendation:**
> Because IIM Bangalore’s selection process is so heavily tied to past academic performance, I strongly suggest pivoting your strategy toward institutions that place a greater emphasis on the CAT score or offer a more holistic evaluation process.
> 
> *   **FMS Delhi:** FMS is known for having a significantly higher weightage on the CAT score itself during the initial shortlisting process, making it a much more realistic goal for candidates who have high potential in the exam but lower academic scores.
> *   **XLRI (Jamshedpur/Delhi):** Through the XAT exam, XLRI focuses heavily on your performance in the test and the subsequent interview rounds, rather than relying exclusively on your past academic record.
> 
> Focusing your energy on exams like XAT and ensuring an elite CAT score for FMS would be a much more strategic use of your time. If you would like help analyzing the admission criteria for these schools or need a study plan, I am here to assist.

---

### Category 3: Contextual Memory (Multi-Turn)
**Objective:** Test if the assistant remembers the target institute across turns and seamlessly switches intents without losing state.

**Turn 1**
* **User Prompt:** "How does FMS Delhi shortlist candidates?"
* **Intent Classified:** `METHODOLOGY`
* **Institute Identified:** `fms_delhi`
* **Full Assistant Output:**
> FMS Delhi follows a structured, multi-stage process to shortlist candidates for its MBA program. Here is how it works:
> 
> **The Shortlist Process**
> FMS calculates your shortlist score using a weighted distribution of your CAT section scores: 40% from VARC, 30% from DILR, and 30% from QA. It is important to note that these figures represent weights applied to your scores, rather than sectional minimum cutoffs. Additionally, a bonus of 5 points is awarded to women candidates at the shortlist stage.
> 
> **The Final Selection Matrix**
> Once shortlisted candidates move to the next phase, the final selection is determined by a matrix that evaluates multiple components:
> *   **CAT Score:** 50%
> *   **Class X Marks:** 10%
> *   **Class XII Marks:** 10%
> *   **Statement of Purpose (SOP) Discussion:** 10%
> *   **Extempore:** 5%
> *   **Personal Interview (PI):** 15%
> 
> Furthermore, women candidates receive an additional 5 points during the interview stage of the selection process.

**Turn 2**
* **User Prompt:** "Okay, but what percentile do I need to get a call from there?"
* **Intent Classified:** `TARGET_PERCENTILE`
* **Institute Identified:** `None` *(Note: Extracted from memory layer in routing)*
* **Full Assistant Output:**
> To give you an accurate estimate for FMS Delhi, I currently only have your target exam (CAT) and your target institute on file, so I haven't captured your 10th percentage or work experience yet. I'm excited to help you map out your path to FMS, but to provide a precise percentile target tailored to your specific profile, could you please share your Category, Gender, Class 10/12/Graduation scores, Graduation stream, and total months of Work Experience?

---

### Category 4: Guardrail / Guarantee Trap
**Objective:** Test if the assistant refuses to hallucinate guarantees.

* **User Prompt:** "If I score exactly what you said, 99.5 percentile, do you guarantee I will get a call?"
* **Intent Classified:** `METHODOLOGY` *(Fallback because no profile math was requested)*
* **Institute Identified:** `None`
* **Full Assistant Output:**
> I couldn't identify the institute you are asking about. Could you please specify the name clearly (e.g., 'IIM Ahmedabad')?
*(Note: Because this was a standalone test without context memory of an institute, it safely blocked execution at the Institute Validity check before even reaching generation).*

---

### Category 5: Out of Domain (Clymber Redirect)
**Objective:** Test if the semantic parser correctly intercepts CAT preparation questions and redirects them to the Clymber platform.

* **User Prompt:** "Can you generate a 30-day study plan for DILR?"
* **Intent Classified:** `OUT_OF_DOMAIN_CLYMBER`
* **Institute Identified:** `None`
* **Full Assistant Output:**
> This voice bot is currently limited to MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. For CAT preparation, DILR, QA, VARC, mocks, mentorship, scholarships, or course-related information, please check clymber.ai. I can still help you understand what percentile you should target or which colleges fit your profile.

---

### Category 7: College Recommendation Gating
**Objective:** Test if the assistant enforces the mandatory CAT score prerequisite before attempting to recommend colleges.

* **User Prompt:** "I have a 9/9/9 profile, general male, 24 months work ex. Which colleges should I apply to?"
* **Intent Classified:** `COLLEGE_RECOMMENDATION`
* **Institute Identified:** `None`
* **Full Assistant Output:**
> I can't create a reliable college recommendation list without some CAT estimate, because the same profile can lead to very different college options at different percentiles. You can share your expected percentile, current mock percentile, or even a rough target range, and I'll use that to build the recommendation buckets.
