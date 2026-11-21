# Medicaid Rejections

AI knowledge base — Medicaid-specific rejection scenarios optimized for RAG retrieval.

> **Disclaimer:** independent personal project. No PHI, no PII, and no Medicaid, agency, or other non-public data is used. Every scenario below is invented, and the rules described are general, public Medicaid rules, not any one state's or agency's procedures. See the full disclaimer in the [README](../README.md#disclaimer).

These scenarios are the **Medicaid specialty layer**: denials that happen because of how Medicaid works (payer of last resort, spend-down, retro eligibility, managed care, provider enrollment, the drug rebate program). Exact rules and limits vary by state, so the copilot treats them as things to verify, not as fixed answers.

---

### RJ-051 – Spend-Down Not Met
**Code:** MCD-001  
**CARC:** 178 (Confirmed; payer scope: medicaid)  
**Severity:** High  
**Sub-Category:** Spend-Down

**Scenario:**  
Member qualifies for Medicaid only after meeting a monthly spend-down. Clinic visit on 03-Apr-2026; the member's medical bills for April didn't reach the spend-down amount until 18-Apr-2026.

---

**Patient Explanation**

1. **What happened:** Your Medicaid coverage for April hadn't started yet when you had this visit, because your spend-down for the month wasn't met yet.
2. **What it means for you:** This bill can count toward your spend-down, and you may owe part of it.
3. **What you should do next:** Give the Medicaid office proof of your medical bills for the month so they can record when your spend-down was met.

---

**Provider Action**

1. **Likely cause:** Service happened before the member met the spend-down for that period.
2. **What to verify:** The date the spend-down was met, and whether this claim's amount was counted toward it.
3. **Next action:** Bill the patient for the part counted toward spend-down; resubmit any remainder once the spend-down-met date is on file.

---

**Analyst Notes**

1. **Interpretation:** Eligibility exists for the month but only from the spend-down-met date; DOS < met date.
2. **Likely issue area:** Eligibility (conditional coverage).
3. **Technical notes:** MCD-001; eligibility segment start = spend-down-met date, not the first of the month.
4. **Next debugging step:** Re-run the date-of-service check after the spend-down-met date is posted.

---

**Keywords:** medicaid, spend-down, medically needy, share of cost, conditional eligibility, DOS

---

### RJ-052 – Patient Liability Deducted
**Code:** MCD-002  
**CARC:** 142 (Confirmed; payer scope: medicaid)  
**Severity:** Medium  
**Sub-Category:** Patient Liability

**Scenario:**  
Nursing facility bills a full month of care for a resident. Medicaid pays less than expected because the resident's monthly patient liability (the resident's own share from their income) was subtracted.

---

**Patient Explanation**

1. **What happened:** Part of this month's care is your share to pay, based on your income.
2. **What it means for you:** Medicaid paid the rest; your share is owed to the facility.
3. **What you should do next:** Pay your monthly share to the facility as arranged.

---

**Provider Action**

1. **Likely cause:** The resident has a monthly patient liability amount on file.
2. **What to verify:** That the liability amount matches the latest notice and was applied only once for the month.
3. **Next action:** Collect the liability from the resident; no resubmission unless the amount applied was wrong.

---

**Analyst Notes**

1. **Interpretation:** Not a true denial; an adjustment for the member's share.
2. **Likely issue area:** Payment calculation.
3. **Technical notes:** MCD-002; adjustment group is usually patient responsibility.
4. **Next debugging step:** Check whether liability was applied twice when a month is split across two claims.

---

**Keywords:** medicaid, patient liability, nursing facility, long-term care, share of cost, adjustment

---

### RJ-053 – Timely Filing Limit Exceeded
**Code:** MCD-003  
**CARC:** 29 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Timely Filing

**Scenario:**  
Office visit on 10-Jan-2025; claim first submitted on 14-Feb-2026, 400 days later, past the 12-month limit.

---

**Patient Explanation**

1. **What happened:** Your provider sent this bill after the deadline.
2. **What it means for you:** In most cases, you can't be billed for a claim the provider filed late.
3. **What you should do next:** Nothing, unless you get a bill; if so, ask the provider about it.

---

**Provider Action**

1. **Likely cause:** Claim submitted after the filing limit.
2. **What to verify:** Proof of an earlier on-time submission, and whether an exception applies (for example, eligibility granted retroactively).
3. **Next action:** Appeal with proof if you have it; otherwise write off.

---

**Analyst Notes**

1. **Interpretation:** Days from DOS to submission > filing limit.
2. **Likely issue area:** Billing workflow.
3. **Technical notes:** MCD-003; federal Medicaid rule is 12 months from the date of service (42 CFR 447.45(d)); states and plans may differ. Checked by `copilot/checks/dos_check.py`.
4. **Next debugging step:** Track how long claims sit before first submission.

---

**Keywords:** timely filing, filing limit, late claim, 12 months, appeal, write off

---

### RJ-054 – Retroactive Eligibility Granted After Denial
**Code:** MCD-004  
**CARC:** 26 (Confirmed; payer scope: medicaid)  
**Severity:** Medium  
**Sub-Category:** Retro Eligibility

**Scenario:**  
ER visit on 15-Jan-2026 denied because the patient had no Medicaid on file. On 20-Mar-2026 the application was approved with coverage back to 01-Jan-2026.

---

**Patient Explanation**

1. **What happened:** When the hospital first billed, your Medicaid wasn't approved yet.
2. **What it means for you:** Your approval now covers that visit, so Medicaid can pay it.
3. **What you should do next:** Give the hospital your Medicaid ID if they ask for it.

---

**Provider Action**

1. **Likely cause:** Claim was billed before the eligibility approval was posted.
2. **What to verify:** That eligibility now covers the DOS, and the filing deadline that applies to retro-eligible claims.
3. **Next action:** Resubmit as is now that eligibility is on file.

---

**Analyst Notes**

1. **Interpretation:** The original denial was correct then but is contradicted by current data.
2. **Likely issue area:** Eligibility timing.
3. **Technical notes:** MCD-004; Medicaid can cover up to three months before the application month. The date-of-service check flags this when `denial_carc` is an eligibility code but coverage now exists on the DOS.
4. **Next debugging step:** Re-check eligibility on denied claims when new eligibility segments arrive.

---

**Keywords:** retro eligibility, retroactive coverage, eligibility approved, resubmit, contradicts denial

---

### RJ-055 – Other Insurance Must Pay First (TPL)
**Code:** MCD-005  
**CARC:** 22 + RARC MA04 (Confirmed; payer scope: medicaid)  
**Severity:** High  
**Sub-Category:** Third-Party Liability

**Scenario:**  
Member has employer coverage on file as primary. Clinic billed Medicaid directly on 02-Feb-2026 without the primary insurer's payment information.

---

**Patient Explanation**

1. **What happened:** You have other insurance, and it has to be billed before Medicaid.
2. **What it means for you:** Medicaid will look at the bill after your other insurance does.
3. **What you should do next:** Make sure the provider has your other insurance card.

---

**Provider Action**

1. **Likely cause:** Medicaid is the payer of last resort; the primary insurer wasn't billed first.
2. **What to verify:** The other coverage on file and its dates; if it ended, ask to have the record updated.
3. **Next action:** Bill the primary insurer, then submit to Medicaid with the primary payment details.

---

**Analyst Notes**

1. **Interpretation:** Coordination of benefits: other coverage active on DOS, no primary payment info on the claim.
2. **Likely issue area:** Third-party liability.
3. **Technical notes:** MCD-005; MA04 says secondary payment needs the primary payer's information (42 CFR 433.139).
4. **Next debugging step:** Flag claims with active other coverage and no primary payment before submission.

---

**Keywords:** TPL, third-party liability, other insurance, coordination of benefits, payer of last resort, primary EOB

---

### RJ-056 – Billed Fee-for-Service; Member in Managed Care
**Code:** MCD-006  
**CARC:** 24 (Confirmed; payer scope: medicaid)  
**Severity:** High  
**Sub-Category:** Managed Care Enrollment

**Scenario:**  
Clinic billed state Medicaid fee-for-service for a 12-Mar-2026 visit, but on that date the member was enrolled in a Medicaid managed care plan.

---

**Patient Explanation**

1. **What happened:** Your Medicaid benefits are handled by a health plan, and the bill went to the wrong place.
2. **What it means for you:** Nothing changes for you; the provider just needs to bill your plan.
3. **What you should do next:** Show the provider your health plan card at your next visit.

---

**Provider Action**

1. **Likely cause:** Member was in a managed care plan on the DOS.
2. **What to verify:** Which plan the member was enrolled in on the DOS (not today).
3. **Next action:** Bill the managed care plan; check whether the provider is in that plan's network.

---

**Analyst Notes**

1. **Interpretation:** Wrong payer: managed care enrollment segment covers the DOS.
2. **Likely issue area:** Eligibility / enrollment.
3. **Technical notes:** MCD-006; uses the same date-of-service logic as plan changes.
4. **Next debugging step:** Check managed care enrollment on the DOS before choosing the payer.

---

**Keywords:** managed care, MCO, fee-for-service, FFS, capitation, wrong payer

---

### RJ-057 – Provider Revalidation Lapsed
**Code:** MCD-007  
**CARC:** B7 (Confirmed; payer scope: medicaid)  
**Severity:** High  
**Sub-Category:** Provider Enrollment

**Scenario:**  
Therapist's Medicaid enrollment was due for revalidation by 31-Dec-2025 and wasn't completed. Services billed for January 2026 were denied.

---

**Patient Explanation**

1. **What happened:** Your provider's Medicaid paperwork was out of date when you were seen.
2. **What it means for you:** This is between the provider and Medicaid.
3. **What you should do next:** Nothing for now; ask the provider if you get a bill.

---

**Provider Action**

1. **Likely cause:** Enrollment lapsed because revalidation wasn't finished on time.
2. **What to verify:** Revalidation status and whether reinstatement is retroactive to the lapse.
3. **Next action:** Complete revalidation; resubmit only for dates the reinstatement covers.

---

**Analyst Notes**

1. **Interpretation:** Provider not eligible to be paid on the DOS.
2. **Likely issue area:** Provider enrollment.
3. **Technical notes:** MCD-007; Medicaid requires providers to revalidate at least every 5 years (42 CFR 455.414).
4. **Next debugging step:** Alert on revalidation deadlines 90 days ahead.

---

**Keywords:** revalidation, provider enrollment, enrollment lapse, B7, reinstatement

---

### RJ-058 – Drug Not Covered: No Rebate Agreement
**Code:** MCD-008  
**CARC:** 211 (Confirmed; payer scope: medicaid)  
**Severity:** Medium  
**Sub-Category:** Pharmacy

**Scenario:**  
Pharmacy claim on 05-May-2026 for a drug whose manufacturer isn't in the Medicaid Drug Rebate Program.

---

**Patient Explanation**

1. **What happened:** Medicaid doesn't cover this particular version of the drug.
2. **What it means for you:** A covered version or a similar drug may be available.
3. **What you should do next:** Ask your pharmacist or doctor about a covered alternative.

---

**Provider Action**

1. **Likely cause:** The NDC isn't eligible for rebate, so Medicaid doesn't cover it.
2. **What to verify:** Whether another manufacturer's version (a different NDC) is rebatable.
3. **Next action:** Dispense a covered alternative, or ask the prescriber about one.

---

**Analyst Notes**

1. **Interpretation:** Coverage depends on the manufacturer's rebate agreement, not just the drug.
2. **Likely issue area:** Pharmacy coverage.
3. **Technical notes:** MCD-008; see the public Medicaid Drug Rebate Program on medicaid.gov.
4. **Next debugging step:** Check the NDC against the public rebate product list before dispensing.

---

**Keywords:** pharmacy, NDC, drug rebate, non-rebatable, manufacturer, Medicaid drug coverage
