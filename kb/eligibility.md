# Eligibility Rejections

AI knowledge base — eligibility rejections scenarios optimized for RAG retrieval.

---

### RJ-001 – Policy Lapsed on Date of Service
**Code:** ELG-001  
**CARC:** 200 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Policy Status

**Scenario:**  
Patient was treated on 10-Mar-2026, but policy expired on 28-Feb-2026 due to non-payment of premium.

---

**Patient Explanation**

1. **What happened:** Your insurance was inactive on the day you received care.
2. **What it means for you:** The visit isn't covered because the plan had lapsed for non-payment.
3. **What you should do next:** Contact your insurer to reinstate the policy; future visits will be covered once active.

---

**Provider Action**

1. **Likely cause:** Premium not paid; coverage lapsed before service date.
2. **What to verify:** Confirm policy status on DOS and any reinstatement effective date.
3. **Next action:** Advise patient to reinstate; resubmit only if retro-effective coverage covers DOS.

---

**Analyst Notes**

1. **Interpretation:** Eligibility check failed — policy_status=LAPSED with lapse_date < DOS.
2. **Likely issue area:** Member coverage / billing cycle.
3. **Technical notes:** Rule ELG-001 triggered; root cause = premium non-payment.
4. **Next debugging step:** Monitor reinstatement events to enable auto-resubmission.

---

**Keywords:** eligibility, policy lapse, inactive coverage, premium non-payment, reinstatement, DOS

---

### RJ-002 – Service Before Policy Effective Date
**Code:** ELG-002  
**CARC:** 26 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Coverage Period

**Scenario:**  
Surgery performed on 05-Jan-2026; policy effective date is 01-Feb-2026.

---

**Patient Explanation**

1. **What happened:** Your plan hadn't started when this service was provided.
2. **What it means for you:** It can't be billed to this policy because coverage began later.
3. **What you should do next:** Check if a previous insurance plan covered the service date.

---

**Provider Action**

1. **Likely cause:** Service performed before plan start.
2. **What to verify:** Confirm correct effective date and look up prior carrier.
3. **Next action:** Rebill to the carrier covering DOS.

---

**Analyst Notes**

1. **Interpretation:** Temporal violation: DOS < effective_date.
2. **Likely issue area:** Eligibility / plan switching boundary.
3. **Technical notes:** ELG-002 triggered at intake validation.
4. **Next debugging step:** Flag claims at plan-switch boundaries for prior-carrier lookup.

---

**Keywords:** eligibility, effective date, coverage period, prior carrier, plan switch

---

### RJ-003 – Member ID Not Found
**Code:** ELG-003  
**CARC:** 31 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Member Verification

**Scenario:**  
Submitted member ID 'MBR-993821' does not exist in payer master records.

---

**Patient Explanation**

1. **What happened:** The member ID on the claim isn't in our system.
2. **What it means for you:** We can't match the claim to a member record.
3. **What you should do next:** Check your insurance card and resend the correct ID.

---

**Provider Action**

1. **Likely cause:** Wrong, mistyped, or stale member ID submitted.
2. **What to verify:** Verify ID against patient's current insurance card.
3. **Next action:** Resubmit with correct ID format.

---

**Analyst Notes**

1. **Interpretation:** Identifier lookup miss in eligibility master.
2. **Likely issue area:** Member identification / data entry.
3. **Technical notes:** ELG-003; possible causes: typo, format, unregistered member.
4. **Next debugging step:** Add to member-match failure queue for manual review.

---

**Keywords:** eligibility, member ID, lookup miss, identifier, verification

---

### RJ-004 – Dependent Exceeds Age Limit
**Code:** ELG-004  
**CARC:** 32 (Confirmed; payer scope: commercial)  
**Severity:** Medium  
**Sub-Category:** Dependent Coverage

**Scenario:**  
Claim for dependent child aged 27; plan covers dependents up to age 26.

---

**Patient Explanation**

1. **What happened:** This plan only covers dependents up to age 26.
2. **What it means for you:** The dependent is now too old to be covered under this policy.
3. **What you should do next:** Look into individual or marketplace plans for them.

---

**Provider Action**

1. **Likely cause:** Dependent has aged out of the plan.
2. **What to verify:** Confirm dependent's date of birth and plan's age cap.
3. **Next action:** Mark as non-covered dependent; advise alternate coverage.

---

**Analyst Notes**

1. **Interpretation:** Dependent eligibility breach: age=27, cap=26.
2. **Likely issue area:** Dependent rules / age policy.
3. **Technical notes:** ELG-004; deterministic rule.
4. **Next debugging step:** Add member_age_at_DOS to preflight validation.

---

**Keywords:** eligibility, dependent, age limit, age cap, ineligible dependent

---

### RJ-005 – Annual Benefit Maximum Exceeded
**Code:** ELG-005  
**CARC:** 119 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Benefit Exhaustion

**Scenario:**  
Patient has used all 20 covered physiotherapy sessions for the year.

---

**Patient Explanation**

1. **What happened:** You've used all sessions your plan covers this year.
2. **What it means for you:** New sessions won't be covered until benefits reset.
3. **What you should do next:** Wait for plan renewal or pay out of pocket until then.

---

**Provider Action**

1. **Likely cause:** Annual benefit cap reached.
2. **What to verify:** Confirm session count and plan reset date.
3. **Next action:** Bill remaining services to patient or hold until reset.

---

**Analyst Notes**

1. **Interpretation:** Benefit counter at limit: used=20, allowed=20.
2. **Likely issue area:** Benefit utilization tracking.
3. **Technical notes:** ELG-005; counter saturation.
4. **Next debugging step:** Track benefit utilization in real time and warn before final session.

---

**Keywords:** eligibility, benefit limit, annual maximum, physiotherapy, benefit reset

---

### RJ-006 – Service Within Waiting Period
**Code:** ELG-006  
**CARC:** 179 (Confirmed; payer scope: commercial)  
**Severity:** High  
**Sub-Category:** Waiting Period

**Scenario:**  
Maternity claim 4 months after enrollment; plan has a 9-month maternity waiting period.

---

**Patient Explanation**

1. **What happened:** Your plan has a 9-month maternity waiting period.
2. **What it means for you:** This visit happened before the waiting period ended.
3. **What you should do next:** Maternity benefits become active after the waiting period.

---

**Provider Action**

1. **Likely cause:** Service performed inside contractual waiting period.
2. **What to verify:** Confirm enrollment date and benefit waiting periods.
3. **Next action:** Inform patient of earliest covered DOS.

---

**Analyst Notes**

1. **Interpretation:** Waiting-period rule fired: elapsed_months=4, required=9.
2. **Likely issue area:** Benefit-start timing.
3. **Technical notes:** ELG-006; deterministic threshold.
4. **Next debugging step:** Show benefit-start countdown in member portal.

---

**Keywords:** eligibility, waiting period, maternity, benefit start, exclusion window

---

### RJ-007 – Service Excluded Under Plan
**Code:** ELG-007  
**CARC:** 204 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Plan Exclusion

**Scenario:**  
Cosmetic rhinoplasty under a plan that excludes cosmetic procedures.

---

**Patient Explanation**

1. **What happened:** This plan doesn't cover cosmetic procedures.
2. **What it means for you:** The service is outside the plan's covered benefits.
3. **What you should do next:** If medically required, your doctor can submit an appeal with supporting notes.

---

**Provider Action**

1. **Likely cause:** Procedure on plan exclusion list.
2. **What to verify:** Check exclusion clause and any medical-necessity exceptions.
3. **Next action:** Submit appeal with diagnosis supporting medical necessity.

---

**Analyst Notes**

1. **Interpretation:** Exclusion-list hit on 'cosmetic' keyword.
2. **Likely issue area:** Plan benefits / exclusions.
3. **Technical notes:** ELG-007; rule-based exclusion match.
4. **Next debugging step:** Add LLM-based necessity check for borderline cases.

---

**Keywords:** eligibility, plan exclusion, cosmetic, non-covered service, appeal

---

### RJ-008 – Coverage Ended With Employment
**Code:** ELG-008  
**CARC:** 27 (Confirmed; payer scope: commercial)  
**Severity:** High  
**Sub-Category:** Termination

**Scenario:**  
DOS 15-Apr-2026; employer coverage ended 31-Mar-2026.

---

**Patient Explanation**

1. **What happened:** Your insurance through your employer ended before this visit.
2. **What it means for you:** The visit isn't covered because the plan was already terminated.
3. **What you should do next:** Look into COBRA or a marketplace plan for continued coverage.

---

**Provider Action**

1. **Likely cause:** Group coverage terminated due to employment end.
2. **What to verify:** Verify termination date from employer/HR feed.
3. **Next action:** Educate patient on COBRA / marketplace options.

---

**Analyst Notes**

1. **Interpretation:** Coverage window closed: term_date < DOS.
2. **Likely issue area:** Group coverage / HR feed.
3. **Technical notes:** ELG-008; sourced from employer termination feed.
4. **Next debugging step:** Link employment events to eligibility cache for same-day updates.

---

**Keywords:** eligibility, termination, employment ended, COBRA, group coverage

---

### RJ-009 – Multiple Active Primary Policies
**Code:** ELG-009  
**CARC:** 22 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Duplicate Enrollment

**Scenario:**  
Member has active coverage under two employer groups; COB required.

---

**Patient Explanation**

1. **What happened:** You have two active insurance plans.
2. **What it means for you:** We need to know which plan pays first before processing.
3. **What you should do next:** Contact your insurers to confirm primary vs secondary order.

---

**Provider Action**

1. **Likely cause:** Two active primary policies detected.
2. **What to verify:** Confirm COB order via birthday rule or employer rule.
3. **Next action:** Hold claim and trigger COB workflow.

---

**Analyst Notes**

1. **Interpretation:** Dual primary coverage on file.
2. **Likely issue area:** Coordination of Benefits.
3. **Technical notes:** ELG-009; check latest COB questionnaire.
4. **Next debugging step:** Trigger COB workflow and resolve primary payer.

---

**Keywords:** eligibility, coordination of benefits, COB, dual coverage, primary payer

---

### RJ-010 – Pre-existing Condition in Exclusion Window
**Code:** ELG-010  
**CARC:** 51 (Dropped (not used in v1); payer scope: commercial)  
**Severity:** High  
**Sub-Category:** Pre-existing Condition

**Scenario:**  
Diabetes-related claim within 24-month pre-existing condition exclusion period.

---

**Patient Explanation**

1. **What happened:** Your plan has a waiting period for pre-existing conditions.
2. **What it means for you:** This claim falls inside that window, so it isn't covered yet.
3. **What you should do next:** It will be covered after the waiting period ends.

---

**Provider Action**

1. **Likely cause:** Condition predates enrollment and falls within exclusion window.
2. **What to verify:** Confirm condition history and enrollment date.
3. **Next action:** Note earliest covered DOS to patient.

---

**Analyst Notes**

1. **Interpretation:** Pre-ex rule: enrollment_date + 24mo > DOS.
2. **Likely issue area:** Pre-existing condition policy.
3. **Technical notes:** ELG-010; condition-to-enrollment timeline check.
4. **Next debugging step:** Add condition-to-enrollment timeline check at intake.

---

**Keywords:** eligibility, pre-existing condition, exclusion window, waiting period, diabetes

---

### RJ-011 – Service Outside Coverage Territory
**Code:** ELG-011  
**CARC:** 158 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Geographic Coverage

**Scenario:**  
Treatment received abroad; plan covers domestic services only.

---

**Patient Explanation**

1. **What happened:** Your plan only covers care inside the country.
2. **What it means for you:** This visit happened abroad and isn't covered.
3. **What you should do next:** Travel insurance can help for future trips abroad.

---

**Provider Action**

1. **Likely cause:** Out-of-territory service without travel rider.
2. **What to verify:** Confirm location and any travel rider on file.
3. **Next action:** Decline non-payable; suggest travel coverage.

---

**Analyst Notes**

1. **Interpretation:** Geo-rule breach: service_country != coverage_country.
2. **Likely issue area:** Geographic / territorial rules.
3. **Technical notes:** ELG-011; territory check.
4. **Next debugging step:** Flag OON-geo at intake form before submission.

---

**Keywords:** eligibility, geographic coverage, international, travel rider, territory

---

### RJ-012 – Service Not in Plan Tier
**Code:** ELG-012  
**CARC:** 204 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Plan Type Mismatch

**Scenario:**  
Dental implant billed under medical-only plan with no dental rider.

---

**Patient Explanation**

1. **What happened:** Your plan covers medical care, not dental.
2. **What it means for you:** This procedure needs a separate dental plan.
3. **What you should do next:** Add a dental plan or rider at next enrollment.

---

**Provider Action**

1. **Likely cause:** Service category not in member's plan benefits.
2. **What to verify:** Confirm plan benefit categories.
3. **Next action:** Recommend dental plan upgrade.

---

**Analyst Notes**

1. **Interpretation:** Plan-product mismatch on benefit category.
2. **Likely issue area:** Plan benefit categories.
3. **Technical notes:** ELG-012; benefit-category lookup failed.
4. **Next debugging step:** Add pre-submission benefit-category check.

---

**Keywords:** eligibility, plan tier, dental, non-covered category, rider

---

### RJ-013 – Retroactive Coverage Cancellation
**Code:** ELG-013  
**CARC:** 27 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Retroactive Termination

**Scenario:**  
Policy cancelled retroactively to 01-Jan-2026; DOS is 20-Feb-2026.

---

**Patient Explanation**

1. **What happened:** Your insurance was cancelled going back to earlier this year.
2. **What it means for you:** This visit is no longer covered under the plan.
3. **What you should do next:** Contact your insurer to confirm reasons and next steps.

---

**Provider Action**

1. **Likely cause:** Retro-termination voids coverage on DOS.
2. **What to verify:** Confirm retro-term effective date with payer.
3. **Next action:** Resubmit to alternate carrier if available.

---

**Analyst Notes**

1. **Interpretation:** Retro-term: retro_date < DOS.
2. **Likely issue area:** Retroactive eligibility events.
3. **Technical notes:** ELG-013; impacts prior paid claims in range.
4. **Next debugging step:** Auto-recall paid claims in retro-term range for adjustment.

---

**Keywords:** eligibility, retroactive termination, retro-term, coverage cancellation, claw-back

---
