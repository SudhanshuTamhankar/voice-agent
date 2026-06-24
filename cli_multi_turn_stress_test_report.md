# Voice CLI Multi-Turn Stress Test Report (10 Deep Scenarios, 41 Queries)
This report evaluates the agent's memory and conversational flow across 10 multi-turn scenarios (41 total queries).

## Test Case 1: Methodology
**Description:** FMS Delhi shortlisting to specifics (4 turns)

> **User Speech:** 'how does FMS Delhi shortlist candidates for interview'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> FMS Delhi shortlists candidates for the interview based on a weighted formula that considers their CAT scores. Specifically, the shortlisting score is calculated using 40% from the VARC section, 30% from the DILR section, and 30% from the QA section. Additionally, there is a bonus of +5 points for women candidates during the shortlisting process. 

It's important to note that the weights assigned to the CAT sections are not based on minimum cutoffs. After the shortlisting stage, the final selection process incorporates further components, including academic performance in Class X and XII, SOP discussion, an extempore session, and a personal interview, along with another bonus of +5 for women candidates at the interview stage. 

If you have any more questions, feel free to ask!

> **User Speech:** 'do they have a diversity bonus?'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> FMS Delhi does not have a specific "diversity bonus" in the general sense, but they do offer a women bonus in their admissions process. This bonus adds 5 points to the shortlist score for women applicants and another 5 points at the interview stage.

> **User Speech:** 'what is their final selection criteria?'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> The final selection criteria for FMS Delhi include a weighted combination of several components. These are: 50% from the CAT exam, 10% from Class X marks, 10% from Class XII marks, 10% from a Statement of Purpose (SOP) discussion, 5% from an extempore speech, and 15% from a Personal Interview (PI). Additionally, there is a bonus of 5 points for women at the interview stage. It's important to note that there are no published details on specific cutoffs or minimum scores for these components.

> **User Speech:** 'how does Harvard Business School shortlist candidates?'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

---

## Test Case 2: Methodology
**Description:** IIM Ahmedabad details (4 turns)

> **User Speech:** 'what is the selection criteria for IIM Ahmedabad'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> The selection criteria for IIM Ahmedabad are based on a combination of factors. For domestic applicants, the key components include the CAT exam scores and an Academic Rating composite. 

- For the CAT, the minimum requirements are a total score of 95 or above, and at least 85 in each section for General and EWS candidates. Specific values for other categories and PwD candidates are published separately. 
- For international applicants, there is a GMAT/GMAT Focus route with a requirement of a total score of 665 for GMAT Focus and 720 for the previous GMAT format, along with published section minima.

The Academic Rating (AR) is calculated based on several criteria, including work experience (capped at a maximum of five months), gender diversity points, and academic thresholds that vary by stream and category. 

Lastly, the overall selection process utilizes a Composite Score derived from both the AR and the CAT scores. Various factors, including work experience and gender diversity, can influence this score. 

Please note that while some formulae and specifics are mentioned, exact internal cutoffs or benchmarks beyond published values are not disclosed.

> **User Speech:** 'how do they calculate the academic rating?'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> I'm sorry, I cannot provide a definitive or guaranteed prediction about that. I can only provide mathematical estimates based on historical composite formulas. Let's focus on your target percentile or evaluating your current profile strength.

> **User Speech:** 'do they consider work experience?'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> Yes, IIM Ahmedabad does consider work experience as part of their admissions process. It contributes to the Academic Rating composite, specifically with a calculation of 0.20 times the number of months of work experience (capped at 5).

> **User Speech:** 'does IIM Lucknow have a diversity bonus?'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> IIM Lucknow does take diversity factors into account as part of its composite shortlist score methodology. However, there is no specific information published about a diversity bonus.

---

## Test Case 3: Profile Evaluation
**Description:** Gradual profile building for IIM Indore (5 turns)

> **User Speech:** 'can you evaluate my chances for IIM Indore?'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> I understand you're eager to know your chances for IIM Indore! However, I still need a few more details from you: your Category, Gender, Class 10 Score, Class 12 Score, Graduation Score, Graduation Stream, Work Experience in months, and your Actual Percentile. Providing these will help me give you a more accurate evaluation.

> **User Speech:** 'I got 85 percent in 10th class.'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> You scored 85 percent in your 10th class, which is great! Now, could you please provide your category, gender, class 12 score, graduation score, graduation stream, work experience in months, and actual percentile?

> **User Speech:** 'and 88 percent in 12th class, and I am an engineer.'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> You scored 88.0% in your 12th class, which is great! I appreciate you confirming your engineering background. Could you please share your category, gender, graduation score, work experience in months, and your actual percentile?

> **User Speech:** 'I got 82 in graduation and have 24 months of work experience.'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> You shared that you have 82 in graduation and 24 months of work experience, which is great! Could you please provide your category, gender, and actual percentile?

> **User Speech:** 'I am a general male and my cat percentile is 98.'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> For IIM Indore, your profile is Slightly Below Call Range. The main reason is that while you have some strong academic scores and work experience, some areas could be improved. Your strongest factors are your CAT Score (awarded 53.9), 10th Score (awarded 8.0), 12th Score (awarded 20.0), and Work Experience (awarded 2.0). The main pressure points are Diversity (awarded 0.0). The next step is to wait for the official shortlist or focus on interviews if you feel confident. This is based on composite-score evaluation, so treat it as guidance, not a guaranteed call prediction.

---

## Test Case 4: Profile Evaluation
**Description:** Missing specific details for IIM Kozhikode (4 turns)

> **User Speech:** 'Evaluate my chances for IIM Kozhikode.'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> I have noted your target institute as IIM Kozhikode, but I still need more information to evaluate your chances accurately. Could you please provide your Category, Gender, Class 10 Score, Class 12 Score, Graduation Score, Graduation Stream, Work Experience in Months, and Actual Percentile?

> **User Speech:** 'I have 12 months work experience and 99 percentile.'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> I'm sorry, I cannot provide a definitive or guaranteed prediction about that. I can only provide mathematical estimates based on historical composite formulas. Let's focus on your target percentile or evaluating your current profile strength.

> **User Speech:** 'I am a female with 90 in 10th, 92 in 12th, and 85 in grad.'
> **🤖 Assistant [Intent: PROFILE_EVALUATION]:**
> You have scored 90 in your 10th, 92 in your 12th, and 85 in your graduation, which is impressive! Could you please share your category and graduation stream so I can complete your profile?

> **User Speech:** 'I am a general non-engineer.'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

---

## Test Case 5: Target Percentile
**Description:** Asking for target without profile (4 turns)

> **User Speech:** 'what percentile do I need for IIM Calcutta?'
> **🤖 Assistant [Intent: TARGET_PERCENTILE]:**
> I see that you're targeting CAT for admission to IIM Calcutta—that's a great choice! To help you further, could you please provide your Category, Gender, Class 10 Score, Class 12 Score, Graduation Score, Graduation Stream, and Work Experience in months?

> **User Speech:** 'I am a general female with 90 in 10th and 95 in 12th.'
> **🤖 Assistant [Intent: TARGET_PERCENTILE]:**
> You scored 90.0 in your Class 10 and 95.0 in your Class 12, which is impressive! Could you please provide your Graduation Score, Graduation Stream, and Work Experience in months?

> **User Speech:** 'I got 85 in graduation and I am an engineer.'
> **🤖 Assistant [Intent: TARGET_PERCENTILE]:**
> You scored 85 in your graduation, which is noted. It’s great to see your strong academic performance! Could you please let me know your total work experience in months?

> **User Speech:** 'I have 12 months of work experience.'
> **🤖 Assistant [Intent: TARGET_PERCENTILE]:**
> I'm sorry, I cannot provide a definitive or guaranteed prediction about that. I can only provide mathematical estimates based on historical composite formulas. Let's focus on your target percentile or evaluating your current profile strength.

---

## Test Case 6: Target Percentile
**Description:** Impossible target profile followups (3 turns)

> **User Speech:** 'what percentile do I need for IIM Bangalore? I have 60 in 10th.'
> **🤖 Assistant [Intent: TARGET_PERCENTILE]:**
> You scored 60.0 in your Class 10, which I have noted down. Great to see that! Now, could you please provide your Category, Gender, Class 12 Score, Graduation Score, Graduation Stream, and Work Experience in months to help with the evaluation?

> **User Speech:** 'I also have 60 in 12th, 60 in grad, and 0 work ex.'
> **🤖 Assistant [Intent: TARGET_PERCENTILE]:**
> I’ve noted that you have a Class 10 score of 60.0, a Class 12 score of 60.0, and a Graduation score of 60.0, along with 0 months of work experience. Great that you confirmed your scores! Could you please share your category, gender, and graduation stream so I can help evaluate your profile further?

> **User Speech:** 'I am a general male engineer.'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

---

## Test Case 7: College Recommendation
**Description:** Asking for recommendations blankly (5 turns)

> **User Speech:** 'which colleges should I apply to?'
> **🤖 Assistant [Intent: COLLEGE_RECOMMENDATION]:**
> I can't create a reliable college recommendation list without some CAT estimate, because the same profile can lead to very different college options at different percentiles. You can share your expected percentile, current mock percentile, or even a rough target range, and I'll use that to build the recommendation buckets.

> **User Speech:** 'I am an engineer.'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

> **User Speech:** 'I have an 888 profile.'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

> **User Speech:** 'I have 12 months of work experience and I am an NC-OBC male.'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

> **User Speech:** 'my cat score is 92 percentile.'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

---

## Test Case 8: College Recommendation
**Description:** Asking for colleges, then methodology (4 turns)

> **User Speech:** 'Recommend colleges for me.'
> **🤖 Assistant [Intent: COLLEGE_RECOMMENDATION]:**
> I can't create a reliable college recommendation list without some CAT estimate, because the same profile can lead to very different college options at different percentiles. You can share your expected percentile, current mock percentile, or even a rough target range, and I'll use that to build the recommendation buckets.

> **User Speech:** 'EWS female, arts, 9/9/9, 12 months work ex, 98 percentile.'
> **🤖 Assistant [Intent: COLLEGE_RECOMMENDATION]:**
> Based on your profile, I recommend considering IIM Ahmedabad and IIM Bangalore as your top realistic options. It's important to note that your academic rating is a fixed challenge, but you have the power to improve your composite score, which is crucial for your admissions chances. Focus on enhancing that score, as it can really make a difference in your applications. Good luck!

> **User Speech:** 'Why did you recommend IIM Lucknow?'
> **🤖 Assistant [Intent: COLLEGE_RECOMMENDATION]:**
> I'm sorry, I cannot provide a definitive or guaranteed prediction about that. I can only provide mathematical estimates based on historical composite formulas. Let's focus on your target percentile or evaluating your current profile strength.

> **User Speech:** 'what weight does IIM Bangalore give to work experience?'
> **🤖 Assistant [Intent: METHODOLOGY]:**
> IIM Bangalore gives work experience a weight of 10 in their pre-PI composite score. This means that work experience contributes to the overall evaluation during the admissions process. However, the exact impact can vary based on individual circumstances as outlined in their methodology.

---

## Test Case 9: Out of Domain -> Valid
**Description:** General Trivia to Evaluation (4 turns)

> **User Speech:** 'what is the capital of France?'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

> **User Speech:** 'okay fine. can you give me a study plan for DILR?'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN_CLYMBER]:**
> I'm sorry, I cannot provide a definitive or guaranteed prediction about that. I can only provide mathematical estimates based on historical composite formulas. Let's focus on your target percentile or evaluating your current profile strength.

> **User Speech:** 'I want to apply to IIM Calcutta.'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN_CLYMBER]:**
> I'm sorry, I cannot provide a definitive or guaranteed prediction about that. I can only provide mathematical estimates based on historical composite formulas. Let's focus on your target percentile or evaluating your current profile strength.

> **User Speech:** 'General male engineer, 90/90/90, 24 months work ex, 99.5 percentile.'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN_CLYMBER]:**
> This voice bot is currently limited to MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. For CAT preparation, DILR, QA, VARC, mocks, mentorship, scholarships, or course-related information, please check clymber.ai. I can still help you understand what percentile you should target or which colleges fit your profile.

---

## Test Case 10: Edge Case
**Description:** Garbage input to invalid number recovery (4 turns)

> **User Speech:** 'asdfghjkl'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

> **User Speech:** 'Evaluate my profile for IIM Calcutta. I scored 105 percent in 12th.'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

> **User Speech:** 'Oops, I meant 95 percent in 12th.'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

> **User Speech:** 'General male engineer, 90 in 10th, 85 in grad, 12 months work ex, 99 percentile.'
> **🤖 Assistant [Intent: OUT_OF_DOMAIN]:**
> I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'

---

