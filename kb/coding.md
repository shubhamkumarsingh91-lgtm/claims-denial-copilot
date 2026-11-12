# Coding Rejections

AI knowledge base — coding rejections scenarios optimized for RAG retrieval.

---

### RJ-014 – ICD-10 Code Lacks Specificity
**Code:** COD-001  
**CARC:** 146 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Invalid Code

**Scenario:**  
Claim submitted with ICD-10 'J20' without required 4th/5th digit specificity.

---

**Patient Explanation**

1. **What happened:** A coding detail is missing from your claim.
2. **What it means for you:** It needs to be updated before processing.
3. **What you should do next:** Your provider will resubmit with corrected codes.

---

**Provider Action**

1. **Likely cause:** ICD-10 missing required digits.
2. **What to verify:** Confirm latest ICD-10-CM code per condition.
3. **Next action:** Resubmit with full code specificity (e.g., J20.9).

---

**Analyst Notes**

1. **Interpretation:** Code-granularity violation.
2. **Likely issue area:** ICD-10 coding.
3. **Technical notes:** COD-001; specificity validator missing.
4. **Next debugging step:** Add ICD-10 specificity validator at scrubber stage.

---

**Keywords:** coding, ICD-10, specificity, diagnosis code, scrubber

---

### RJ-015 – Procedure Inconsistent With Diagnosis
**Code:** COD-002  
**CARC:** 11 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** CPT Mismatch

**Scenario:**  
CPT 27447 (knee replacement) billed with diagnosis for upper respiratory infection.

---

**Patient Explanation**

1. **What happened:** The procedure billed doesn't match the visit reason.
2. **What it means for you:** We're reviewing the claim with your provider.
3. **What you should do next:** No action needed from you right now.

---

**Provider Action**

1. **Likely cause:** CPT-ICD clinical mismatch.
2. **What to verify:** Verify correct CPT or matching diagnosis.
3. **Next action:** Reroute for medical necessity review.

---

**Analyst Notes**

1. **Interpretation:** CPT-to-ICD semantic mismatch.
2. **Likely issue area:** Clinical coding logic.
3. **Technical notes:** COD-002; semantic alignment failure.
4. **Next debugging step:** Strengthen pre-submission CPT-ICD logic check.

---

**Keywords:** coding, CPT, ICD-10, medical necessity, mismatch

---

### RJ-016 – Unbundled Procedure Components
**Code:** COD-003  
**CARC:** 236 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Unbundling

**Scenario:**  
Component codes billed separately when a global CPT exists.

---

**Patient Explanation**

1. **What happened:** Some parts of your procedure were billed twice in different ways.
2. **What it means for you:** We're correcting it to bill the full package only.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** NCCI unbundling violation.
2. **What to verify:** Map components to parent global CPT.
3. **Next action:** Reverse component lines and bill global only.

---

**Analyst Notes**

1. **Interpretation:** NCCI edit triggered.
2. **Likely issue area:** Bundling rules / NCCI.
3. **Technical notes:** COD-003; track repeat offenders.
4. **Next debugging step:** Add NCCI bundling check to scrubber.

---

**Keywords:** coding, unbundling, NCCI, global CPT, components

---

### RJ-017 – E&M Level Not Supported
**Code:** COD-004  
**CARC:** 150 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Upcoding

**Scenario:**  
Level 5 E&M billed for a routine follow-up not supported by documentation.

---

**Patient Explanation**

1. **What happened:** The level of care billed seems higher than the notes support.
2. **What it means for you:** We're checking the details with your provider.
3. **What you should do next:** No action needed from you right now.

---

**Provider Action**

1. **Likely cause:** E&M level inconsistent with documentation.
2. **What to verify:** Audit history, exam, and MDM elements.
3. **Next action:** Downcode to supported level.

---

**Analyst Notes**

1. **Interpretation:** E&M level-risk flag.
2. **Likely issue area:** E&M coding / documentation.
3. **Technical notes:** COD-004; track provider trend in fraud-risk scoring.
4. **Next debugging step:** Feed provider trends into fraud-risk model.

---

**Keywords:** coding, E&M, upcoding, documentation, audit

---

### RJ-018 – Missing or Invalid Modifier
**Code:** COD-005  
**CARC:** 4 (Confirmed; payer scope: all)  
**Severity:** Low  
**Sub-Category:** Modifier Error

**Scenario:**  
Bilateral procedure submitted without modifier 50.

---

**Patient Explanation**

1. **What happened:** A small coding detail is missing.
2. **What it means for you:** It's a quick fix on your provider's side.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Required modifier missing or wrong.
2. **What to verify:** Confirm correct modifier (50, LT, RT) per CPT.
3. **Next action:** Append modifier and resubmit.

---

**Analyst Notes**

1. **Interpretation:** Mandatory modifier absent.
2. **Likely issue area:** Modifier rules.
3. **Technical notes:** COD-005; rule-engine should auto-suggest.
4. **Next debugging step:** Auto-suggest modifiers at scrubber stage.

---

**Keywords:** coding, modifier, bilateral, modifier 50, scrubber

---

### RJ-019 – Procedure Conflicts With Gender
**Code:** COD-006  
**CARC:** 7 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Gender Conflict

**Scenario:**  
Hysterectomy CPT billed for a male patient in record.

---

**Patient Explanation**

1. **What happened:** A claim detail doesn't match the patient record.
2. **What it means for you:** We're confirming the information before processing.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Gender-specific code on mismatched record.
2. **What to verify:** Verify patient demographics.
3. **Next action:** Correct demographic or CPT.

---

**Analyst Notes**

1. **Interpretation:** Demographic-code conflict.
2. **Likely issue area:** Patient demographics validation.
3. **Technical notes:** COD-006; common data-entry error.
4. **Next debugging step:** Add gender-CPT compatibility table to validator.

---

**Keywords:** coding, gender mismatch, demographics, CPT validation, data entry

---

### RJ-020 – Procedure Conflicts With Age
**Code:** COD-007  
**CARC:** 6 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Age Conflict

**Scenario:**  
Pediatric vaccination CPT billed for a 55-year-old patient.

---

**Patient Explanation**

1. **What happened:** The procedure code is usually for a different age group.
2. **What it means for you:** We're verifying the record.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Age-specific code outside age range.
2. **What to verify:** Confirm patient age and code.
3. **Next action:** Use age-appropriate CPT.

---

**Analyst Notes**

1. **Interpretation:** Age-CPT conflict.
2. **Likely issue area:** Code-age compatibility.
3. **Technical notes:** COD-007; maintain age-range table per CPT.
4. **Next debugging step:** Validate age ranges at intake.

---

**Keywords:** coding, age mismatch, pediatric, adult immunization, CPT validation

---

### RJ-021 – Mutually Exclusive Procedures
**Code:** COD-008  
**CARC:** 231 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Mutually Exclusive

**Scenario:**  
Two CPT codes billed that cannot be performed in the same session.

---

**Patient Explanation**

1. **What happened:** Two procedures that can't happen together were billed.
2. **What it means for you:** We're asking your provider to clarify.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** NCCI mutually exclusive pair billed together.
2. **What to verify:** Confirm which procedure was actually performed.
3. **Next action:** Remove conflicting CPT, retain primary.

---

**Analyst Notes**

1. **Interpretation:** NCCI MUE/PTP edit triggered.
2. **Likely issue area:** NCCI exclusion pairs.
3. **Technical notes:** COD-008; deterministic pair lookup.
4. **Next debugging step:** Block at pre-submission scrubber via exclusion pair table.

---

**Keywords:** coding, NCCI, mutually exclusive, PTP edit, exclusion pair

---

### RJ-022 – Required Diagnosis Code Missing
**Code:** COD-009  
**CARC:** 16 + RARC M76 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Missing Code

**Scenario:**  
Surgical CPT submitted without any ICD-10 diagnosis attached.

---

**Patient Explanation**

1. **What happened:** The reason for the procedure is missing on the claim.
2. **What it means for you:** Your provider will add the missing detail.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Diagnosis pointer empty.
2. **What to verify:** Confirm and add supporting ICD-10.
3. **Next action:** Resubmit with linked diagnosis.

---

**Analyst Notes**

1. **Interpretation:** Mandatory field null: dx_code.
2. **Likely issue area:** Required-field validation.
3. **Technical notes:** COD-009; hard-block at intake.
4. **Next debugging step:** Enforce diagnosis requirement at intake.

---

**Keywords:** coding, missing diagnosis, ICD-10, required field, intake validation

---

### RJ-023 – Procedure Frequency Exceeded
**Code:** COD-010  
**CARC:** 151 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Frequency Limit

**Scenario:**  
MRI of same body part billed 3 times in 30 days; allowed once per 90 days.

---

**Patient Explanation**

1. **What happened:** This imaging was done more often than your plan allows.
2. **What it means for you:** Future scans will be covered after the allowed gap.
3. **What you should do next:** Talk to your provider about timing of next imaging.

---

**Provider Action**

1. **Likely cause:** Frequency rule exceeded.
2. **What to verify:** Verify medical necessity for repeat imaging.
3. **Next action:** Pay first occurrence; deny excess.

---

**Analyst Notes**

1. **Interpretation:** Frequency rule: count=3, limit=1/90d.
2. **Likely issue area:** Utilization frequency tracking.
3. **Technical notes:** COD-010; track rolling window per CPT/member.
4. **Next debugging step:** Track CPT frequency per member with rolling window.

---

**Keywords:** coding, frequency limit, MRI, utilization, rolling window

---

### RJ-024 – Invalid NDC
**Code:** COD-011  
**CARC:** 16 + RARC M119 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** NDC Error

**Scenario:**  
Pharmacy claim with NDC that does not match FDA registry.

---

**Patient Explanation**

1. **What happened:** The medication code on your claim isn't recognized.
2. **What it means for you:** Your pharmacy will correct and resubmit.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** NDC not in FDA reference data.
2. **What to verify:** Verify NDC from package; check 5-4-2 vs 11-digit format.
3. **Next action:** Resubmit with corrected NDC.

---

**Analyst Notes**

1. **Interpretation:** NDC mismatch vs FDA master.
2. **Likely issue area:** Drug coding / NDC.
3. **Technical notes:** COD-011; refresh NDC reference monthly.
4. **Next debugging step:** Refresh NDC reference data monthly.

---

**Keywords:** coding, NDC, pharmacy, FDA registry, drug code

---

### RJ-025 – Place of Service Mismatch
**Code:** COD-012  
**CARC:** 5 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** POS Mismatch

**Scenario:**  
Inpatient-only CPT billed with outpatient place of service code.

---

**Patient Explanation**

1. **What happened:** Where the service happened doesn't match the procedure type.
2. **What it means for you:** We're checking with your provider.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** POS code inconsistent with CPT setting.
2. **What to verify:** Confirm actual service location.
3. **Next action:** Correct POS or CPT and resubmit.

---

**Analyst Notes**

1. **Interpretation:** POS-CPT compatibility failure.
2. **Likely issue area:** Place of service rules.
3. **Technical notes:** COD-012; add compatibility matrix.
4. **Next debugging step:** Add POS-CPT compatibility matrix to validator.

---

**Keywords:** coding, place of service, POS, inpatient, outpatient

---

### RJ-026 – Invalid Revenue Code for Facility
**Code:** COD-013  
**CARC:** 282 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Revenue Code

**Scenario:**  
Hospital revenue code 0450 (ER) billed by ambulatory surgical center.

---

**Patient Explanation**

1. **What happened:** The facility type and billing code don't match.
2. **What it means for you:** Your provider will correct it.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Revenue code not valid for facility type.
2. **What to verify:** Check rev-code list for ASC.
3. **Next action:** Resubmit with correct revenue code.

---

**Analyst Notes**

1. **Interpretation:** Rev-code / facility-type mismatch.
2. **Likely issue area:** Institutional billing.
3. **Technical notes:** COD-013; maintain rev-code-by-facility matrix.
4. **Next debugging step:** Maintain rev-code-by-facility matrix.

---

**Keywords:** coding, revenue code, facility type, ASC, institutional billing

---
