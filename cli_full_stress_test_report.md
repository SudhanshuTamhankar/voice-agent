# Voice CLI Full Stress Test Report (30+ Queries)
This report contains the raw text output from the `AskResponse` API, simulating the exact transcripts processed by the CLI `voice_chat.py` across all supported intents and edge cases.

## Test Case 1: Methodology
**Description:** Basic shortlisting question

> **User Speech:** 'how does FMS Delhi shortlist candidates for interview'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> FMS Delhi follows a structured process for shortlisting and final selection.

For the initial interview shortlist, the institute uses a weighted CAT score based on the following formula: **0.40 × VARC + 0.30 × DILR + 0.30 × QA**. Additionally, female candidates receive a bonus of +5 points at the shortlist stage. It is important to note that the CAT section values mentioned here represent weights rather than sectional minimum cutoffs.

For the final selection matrix, the evaluation criteria expand to include academic history and performance in the interview rounds:
*   **CAT Score:** 50%
*   **Class X Marks:** 10%
*   **Class XII Marks:** 10%
*   **SOP Discussion:** 10%
*   **Extempore:** 5%
*   **Personal Interview (PI):** 15%

Furthermore, female candidates receive an additional +5 bonus at the interview stage of the final selection process.

---

## Test Case 2: Methodology
**Description:** Specific criteria question

> **User Speech:** 'what is the selection criteria for IIM Ahmedabad'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> IIM Ahmedabad determines its candidate selection through two distinct phases: the initial shortlisting process and the final selection.

**Initial Shortlisting Criteria**
For the domestic route, the institute uses a composite score based on your CAT performance and an Academic Rating (AR). 
*   **CAT Cutoffs:** For General/EWS candidates, the requirement is a minimum of 95 overall percentile, with sectional cutoffs of at least 85. Separate cutoffs are published for other categories and PwD candidates.
*   **Academic Rating (AR):** This is calculated as AR = A+B+C+D+E, which incorporates academic thresholds. Specifically, IIM Ahmedabad utilizes stream-wise P thresholds and an 80th-percentile bachelor’s threshold based on your category and academic group.
*   **Diversity and Experience:** The score includes points for gender diversity (3 points for all genders except male) and work experience, which is calculated as 0.20 × (months - 11), capped at a maximum of 5 points.
*   **Composite Score Formula:** Your initial ranking is determined by the formula: CS = 0.35×(AR/38) + 0.65×(CAT/204).

For international applicants, IIM Ahmedabad utilizes a separate overseas route. This requires a GMAT Focus total score of 665 (or a previous GMAT total of 720), alongside specific sectional minimums.

**Final Selection Matrix**
Regarding the final selection criteria (post-shortlist), please note that there is a lack of verified published data. Therefore, specific weightages or formulas for the final selection phase are not publicly disclosed.

---

## Test Case 3: Methodology
**Description:** Asking about specific weights

> **User Speech:** 'what weight does IIM Bangalore give to work experience'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> IIM Bangalore assigns a weight of **10 points** to Work Experience (or a professional course) within its Pre-PI composite score calculation.

The scoring for this component is determined by the following formula:
*   For experience of less than 36 months ($x < 36$), the score is calculated as $10x/36$.
*   For experience of 36 months or more ($x \ge 36$), a maximum score of 10 is awarded.

If you have completed a professional course, IIM Bangalore will take the higher of your work experience score or your professional course score when calculating your total.

---

## Test Case 4: Methodology
**Description:** Asking about a specific academic stage

> **User Speech:** 'how important is 10th marks for IIM Calcutta'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> For IIM Calcutta, your 10th-grade marks hold specific weight in the shortlist stage. Here is how it factors into the selection process:

*   **Shortlist Stage (Stage-II):** Your 10th-grade marks account for **10 out of the 85 points** used to determine the shortlist. These points are assigned based on pre-defined scoring brackets (10/8/6/4/2/0). 
*   **Formula:** The Stage-II shortlist formula is: CAT score (56) + Class 10 marks (10) + Class 12 marks (15) + Gender diversity (4).
*   **Important Note:** For the initial Stage-I screening, the process relies on meeting CAT sectional and overall minimum cutoffs (85/80/80/75 for Open category, with category-wise minima). Importantly, graduation marks and work experience carry 0% weight in the shortlist stage.

In summary, while your 10th marks are a direct component of the 85-point shortlist calculation, they are evaluated alongside your CAT performance, 12th-grade marks, and gender diversity.

---

## Test Case 5: Methodology
**Description:** Asking about diversity factors

> **User Speech:** 'does IIM Lucknow have a diversity bonus'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> Yes, IIM Lucknow incorporates diversity into its shortlisting process.

According to the institute's published composite score formula for the initial shortlist, diversity is factored in through two specific components, **DFa** and **DFb**, which each carry a 5% weightage (totaling 10% of your composite score).

The composite shortlist formula is as follows:
**0.60 (Scaled CAT Score) + 0.10 (Class 12 Marks) + 0.10 (Graduation Marks) + 0.10 (Work Experience) + 0.05 (DFa) + 0.05 (DFb)**

Please note that regarding the final selection matrix, there is a lack of verified published data on whether diversity factors continue to hold weight beyond this initial shortlisting stage.

---

## Test Case 6: Methodology
**Description:** Asking about an unsupported institute (Fallback)

> **User Speech:** 'how does Harvard Business School shortlist candidates'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> I couldn't identify the institute you are asking about. Could you please specify the name clearly (e.g., 'IIM Ahmedabad')?

---

## Test Case 7: Profile Evaluation - Standard Flow
**Description:** Evaluating chances for IIM Indore over multiple turns

> **User Speech:** 'can you evaluate my chances for IIM Indore?'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> I would be happy to help you evaluate your chances for IIM Indore, but I still need a bit more information to run the analysis. Could you please provide your Category, Gender, Class 10th and 12th percentages, Graduation score and stream, total months of Work Experience, and your CAT score/percentile so I can give you an accurate assessment?

> **User Speech:** 'I got 85 in 10th 88 in 12th and 82 in graduation. I am an engineer fresher.'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> Thank you for sharing those details—you have a very solid academic foundation! To help me calculate your specific chances for IIM Indore, could you please tell me your category (General/NC-OBC/SC/ST/EWS), your gender, and the actual CAT percentile you have achieved or are targeting?

> **User Speech:** 'I am a general male and my cat percentile is 98'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> For IIM Indore, your profile is Currently Outside Call Range. The main reason is that your composite score, while boosted by a strong CAT performance, does not yet meet the high threshold required for a general male candidate when accounting for the absence of diversity and work experience points. Your strongest factors are CAT Score (awarded 53.9), 10th Score (awarded 8.0), and 12th Score (awarded 20.0). The main pressure points are Diversity (awarded 0.0) and Work Experience (awarded 0.0). The next step is Wait for official shortlist or focus on interviews if confident. This is based on composite-score evaluation, so treat it as guidance, not a guaranteed call prediction.

---

## Test Case 8: Profile Evaluation - Partial Profile
**Description:** Asking for evaluation with extreme missing data

> **User Speech:** 'Is my profile good for IIM Ahmedabad?'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> I would love to help you assess your chances at IIM Ahmedabad, but I currently don't have enough data to run the evaluation. Could you please provide your category, gender, Class 10 and 12 percentages, graduation score and stream, total work experience in months, and your actual CAT percentile so I can give you an accurate assessment?

> **User Speech:** 'I have 99 percent in 10th.'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> That is an exceptional score to start with! To give you a precise evaluation for IIM Ahmedabad, could you please provide your category, gender, Class 12 score, graduation score and stream, total months of work experience, and your actual CAT percentile?

---

## Test Case 9: Profile Evaluation - All at once
**Description:** Providing all details in a single query

> **User Speech:** 'Evaluate my chances for IIM Kozhikode. I am a general female, non-engineer, 9/9/9 profile, 12 months work experience, and 99 percentile.'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> For IIM Kozhikode, your profile is Comfortably Above Benchmark.

The main reason for this label is that your strong academic history and high CAT score, combined with the additional points for diversity and academic consistency, create a very favorable position relative to the institutional selection criteria.

Your strongest factors are CAT Score (awarded 49.5), 10th Score (awarded 13.5), 12th Score (awarded 18.0), Work Experience (awarded 1.67), and Diversity (awarded 10.0).

The main pressure points are None.

The next step is Wait for official shortlist or focus on interviews if confident.

This is based on composite-score evaluation, so treat it as guidance, not a guaranteed call prediction.

---

## Test Case 10: Profile Evaluation - Slang
**Description:** Using slang like '888 profile'

> **User Speech:** 'What are my chances for FMS Delhi with an 888 profile and 95 percentile?'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> That’s a great profile summary, but to give you a precise assessment for FMS, I still need a few more details: could you please let me know your category, gender, graduation stream, and total months of work experience?

---

## Test Case 11: Target Percentile - Multi-turn
**Description:** Asking for target percentile with follow-ups

> **User Speech:** 'what percentile do I need for IIM Calcutta?'
> **🤖 Assistant [Intent: TARGET_PERCENTILE]:**
> To provide you with an accurate target percentile for IIM Calcutta, I still need a bit more context about your academic and professional background. Could you please share your Category, Gender, Class 10 and 12 marks, Graduation score and stream, and your total months of work experience?

> **User Speech:** 'I am a general female with 90 in 10th and 95 in 12th and 85 in graduation. 0 work experience.'
> **🤖 Assistant [Intent: TARGET_PERCENTILE]:**
> That is a fantastic academic profile you've built so far! To help me run a precise calculation for your target of IIM Calcutta, could you please clarify your graduation stream (e.g., Engineering, Arts, Commerce, etc.)?

---

## Test Case 12: Target Percentile - All at once
**Description:** Providing all details upfront

> **User Speech:** 'Target percentile for IIM Lucknow if I am a general male engineer, 8/8/8, and 24 months work experience?'
> **🤖 Assistant [Intent: TARGET_PERCENTILE]:**
> Hello! As your MBA Admissions Assistant, I have carefully analyzed your profile against the historical selection criteria for IIM Lucknow.

I must share some hard news with you regarding your target. Based on the current composite score criteria used by IIM Lucknow, which places significant weight on your past academic records (Class 10, Class 12, and Graduation), your profile faces a mathematical challenge.

Because your academic scores are at a fixed 80/80/80 level, even achieving a perfect 100 percentile in the CAT would not be sufficient to bridge the gap required to reach the safe composite score threshold for an interview call from IIM Lucknow. The selection model heavily favors candidates with more consistent "top-tier" academic excellence throughout their schooling and graduation.

**My recommendation:**
I strongly suggest that you shift your focus toward institutions that prioritize CAT performance over rigid academic consistency. 

*   **FMS Delhi:** They are known for being extremely CAT-centric. If you can score very high on the CAT, your past academic records will have significantly less impact on your chances of receiving an interview call compared to IIM Lucknow.
*   **XLRI (Jamshedpur/Delhi):** They utilize the XAT exam. XLRI places a high value on the entrance exam score and your performance in the subsequent interview rounds, making it an excellent target for someone with your specific work experience and potential to excel in a high-stakes exam.

While IIM Lucknow might be out of reach given the current selection parameters, you possess valuable work experience that will serve you well in the interview processes for other top-tier B-schools. I recommend focusing your efforts on these more "exam-centric" institutes to maximize your chances of success.

---

## Test Case 13: Target Percentile - Impossible Edge Case
**Description:** Mathematically impossible target

> **User Speech:** 'what percentile do I need for IIM Bangalore? I am a general male engineer with 60 in 10th, 60 in 12th, 60 in grad, and 0 work ex.'
> **🤖 Assistant [Intent: TARGET_PERCENTILE]:**
> I understand you are looking to target IIM Bangalore for your MBA. 

Based on an assessment of your profile—specifically your academic history (Class 10, Class 12, and Graduation scores) and your current work experience—I must be transparent with you. 

IIM Bangalore utilizes a very rigorous composite score system for its initial shortlisting process, which assigns significant weight to your past academic performance. Given your current academic scores and the lack of work experience, it is mathematically impossible to reach the required composite score threshold for an interview call, even if you were to achieve a perfect 100 percentile in the CAT.

I know this is not the news you were hoping for, and I want to encourage you not to let this dampen your aspirations. While IIM Bangalore may not be a viable option given their specific selection criteria, there are other prestigious institutions that place a higher emphasis on your CAT performance rather than your past academic consistency.

I strongly recommend that you pivot your focus toward institutes like **FMS Delhi** or **XLRI (via XAT)**. These institutions are known to be more "CAT/XAT-centric" and offer world-class pedagogy and placement outcomes that are on par with, or exceed, many of the IIMs. 

Focusing your energy on excelling in your upcoming entrance exams will allow you to compete effectively for these top-tier programs. You have a path to a top MBA—it just looks a little different than the one you originally envisioned.

---

## Test Case 14: College Recommendation - Standard
**Description:** Asking for recommendations with partial data

> **User Speech:** 'which colleges should I apply to?'
> **🤖 Assistant [Intent: COLLEGE_RECOMMENDATION]:**
> I can't create a reliable college recommendation list without some CAT estimate, because the same profile can lead to very different college options at different percentiles. You can share your expected percentile, current mock percentile, or even a rough target range, and I'll use that to build the recommendation buckets.

> **User Speech:** 'I have a 999 profile general male with 24 months of work experience'
> **🤖 Assistant [Intent: COLLEGE_RECOMMENDATION]:**
> I can't create a reliable college recommendation list without some CAT estimate, because the same profile can lead to very different college options at different percentiles. You can share your expected percentile, current mock percentile, or even a rough target range, and I'll use that to build the recommendation buckets.

> **User Speech:** 'my cat score is 99.56 percentile'
> **🤖 Assistant [Intent: COLLEGE_RECOMMENDATION]:**
> That's an incredible CAT percentile, and with such strong academic consistency across your 10th, 12th, and graduation, you have a very solid foundation! To help me finalize your profile evaluation for the top IIMs, could you please let me know which stream you graduated in?

> **User Speech:** 'I am an engineer'
> **🤖 Assistant [Intent: COLLEGE_RECOMMENDATION]:**
> I'm sorry, I cannot provide a definitive or guaranteed prediction about that. I can only provide mathematical estimates based on historical composite formulas. Let's focus on your target percentile or evaluating your current profile strength.

---

## Test Case 15: College Recommendation - Poor Profile
**Description:** Recommendations for a difficult profile

> **User Speech:** 'Recommend colleges for a 7/7/7 profile, general male engineer, fresher, 90 percentile.'
> **🤖 Assistant [Intent: COLLEGE_RECOMMENDATION]:**
> Based on your profile, FMS Delhi is your strongest match right now, while IIFT Delhi stands out as a solid stretch school. You’re facing a natural disadvantage due to gender diversity benchmarks, which is a fixed factor we can't change. Your primary focus must be boosting your CAT score, as that remains your biggest controllable lever to bridge the gap for those top-tier programs.

---

## Test Case 16: Out of Domain - General Trivia
**Description:** Completely unrelated questions

> **User Speech:** 'what is the capital of France?'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

> **User Speech:** 'how do I bake a cake?'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

---

## Test Case 17: Out of Domain - Clymber Content
**Description:** CAT preparation questions not covered by this specific bot

> **User Speech:** 'can you give me a study plan for DILR?'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN_CLYMBER]:**
> This voice bot is currently limited to MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. For CAT preparation, DILR, QA, VARC, mocks, mentorship, scholarships, or course-related information, please check clymber.ai. I can still help you understand what percentile you should target or which colleges fit your profile.

> **User Speech:** 'how to solve a reading comprehension passage?'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN_CLYMBER]:**
> This voice bot is currently limited to MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. For CAT preparation, DILR, QA, VARC, mocks, mentorship, scholarships, or course-related information, please check clymber.ai. I can still help you understand what percentile you should target or which colleges fit your profile.

> **User Speech:** 'what is the price of the mentorship program?'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN_CLYMBER]:**
> This voice bot is currently limited to MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. For CAT preparation, DILR, QA, VARC, mocks, mentorship, scholarships, or course-related information, please check clymber.ai. I can still help you understand what percentile you should target or which colleges fit your profile.

---

## Test Case 18: Edge Case - Invalid Numbers
**Description:** Providing impossible percentages or months

> **User Speech:** 'Evaluate my profile for IIM Calcutta. I scored 105 percent in 12th.'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> It looks like one of the numbers you provided is out of valid bounds (for example, percentiles must be 100 or below). Could you check and provide it again?

> **User Speech:** 'I have 600 months of work experience.'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> It looks like one of the numbers you provided is out of valid bounds (for example, percentiles must be 100 or below). Could you check and provide it again?

---

## Test Case 19: Edge Case - Vague Query
**Description:** Saying something very vague

> **User Speech:** 'I want an MBA'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> That is a great ambition, and I would be happy to help you map out your path toward the top IIMs! To provide you with a precise evaluation, I need you to share a few more details: your category, gender, Class 10/12 scores, graduation stream and score, total months of work experience, and your actual CAT percentile.

---
