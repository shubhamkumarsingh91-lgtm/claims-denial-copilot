# Authorization Rejections

AI knowledge base — authorization rejections scenarios optimized for RAG retrieval.

---

### RJ-039 – Prior Authorization Not Obtained
**Code:** AUT-001  
**CARC:** 197 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Missing PA

**Scenario:**  
Elective MRI performed with no prior authorization on file.

---

**Patient Explanation**

1. **What happened:** This service needed approval from your insurance before it was done.
2. **What it means for you:** It's currently denied because the approval wasn't requested.
3. **What you should do next:** Ask your doctor about requesting approval after the fact.

---

**Provider Action**

1. **Likely cause:** PA-required CPT performed without PA.
2. **What to verify:** Confirm whether retro-auth is allowed.
3. **Next action:** Submit retro-PA request with clinical notes.

---

**Analyst Notes**

1. **Interpretation:** PA-required CPT + no PA record.
2. **Likely issue area:** Prior authorization.
3. **Technical notes:** AUT-001; maintain PA-required CPT list.
4. **Next debugging step:** Flag PA-required CPTs at scheduling.

---

**Keywords:** authorization, prior auth, PA, MRI, retro-auth

---

### RJ-040 – Prior Authorization Expired
**Code:** AUT-002  
**CARC:** 302 (Verify; payer scope: all)  
**Severity:** High  
**Sub-Category:** Expired PA

**Scenario:**  
PA valid until 28-Feb-2026; service rendered 15-Mar-2026.

---

**Patient Explanation**

1. **What happened:** The approval expired before the visit.
2. **What it means for you:** A new approval is needed.
3. **What you should do next:** Your doctor's office will request a new PA.

---

**Provider Action**

1. **Likely cause:** PA window closed before DOS.
2. **What to verify:** Confirm PA validity dates.
3. **Next action:** Submit new PA request.

---

**Analyst Notes**

1. **Interpretation:** PA window: auth_end < DOS.
2. **Likely issue area:** PA lifecycle.
3. **Technical notes:** AUT-002; add PA-expiry alerts.
4. **Next debugging step:** Add PA-expiry alerts at 7 / 3 / 1 day intervals.

---

**Keywords:** authorization, prior auth, expired PA, auth window, PA renewal

---

### RJ-041 – Authorized Procedure Doesn't Match Billed
**Code:** AUT-003  
**CARC:** 284 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** PA Mismatch

**Scenario:**  
PA for CPT 29881 (knee arthroscopy); claim billed CPT 27447 (total knee replacement).

---

**Patient Explanation**

1. **What happened:** The procedure approved isn't the one performed.
2. **What it means for you:** A new approval is needed for the actual procedure.
3. **What you should do next:** Your doctor's office will handle this.

---

**Provider Action**

1. **Likely cause:** PA tied to a different CPT than billed.
2. **What to verify:** Compare PA CPT vs billed CPT.
3. **Next action:** Initiate utilization review or retro-PA.

---

**Analyst Notes**

1. **Interpretation:** PA-CPT mismatch.
2. **Likely issue area:** Prior authorization scope.
3. **Technical notes:** AUT-003; auto-compare PA CPT vs billed CPT.
4. **Next debugging step:** Auto-compare PA CPT vs billed CPT pre-adjudication.

---

**Keywords:** authorization, PA mismatch, utilization review, retro-auth, CPT

---

### RJ-042 – PA Unit Limit Exceeded
**Code:** AUT-004  
**CARC:** 198 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Unit Limit

**Scenario:**  
PA authorised 10 therapy visits; claim submitted for 14.

---

**Patient Explanation**

1. **What happened:** Your plan approved 10 sessions, but more were done.
2. **What it means for you:** The extra sessions need new approval.
3. **What you should do next:** Your therapist can request approval for the extra visits.

---

**Provider Action**

1. **Likely cause:** Units billed exceed PA-approved units.
2. **What to verify:** Confirm visit count and PA limit.
3. **Next action:** Pay up to approved amount; request PA extension.

---

**Analyst Notes**

1. **Interpretation:** Unit overage: billed - approved = +4.
2. **Likely issue area:** PA unit tracking.
3. **Technical notes:** AUT-004; pro-rate payment to approved units.
4. **Next debugging step:** Pro-rate payment to approved units.

---

**Keywords:** authorization, unit limit, therapy, PA extension, pro-rate

---

### RJ-043 – PA Issued to Different Provider
**Code:** AUT-005  
**CARC:** 296 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Wrong Provider

**Scenario:**  
PA granted to Provider A; service rendered by Provider B.

---

**Patient Explanation**

1. **What happened:** The approval was for a different doctor.
2. **What it means for you:** Approval needs to be transferred or reissued.
3. **What you should do next:** Your provider's office will handle this.

---

**Provider Action**

1. **Likely cause:** PA tied to non-rendering provider.
2. **What to verify:** Validate rendering NPI vs PA record.
3. **Next action:** Request PA transfer/reissue.

---

**Analyst Notes**

1. **Interpretation:** Provider-PA linkage mismatch.
2. **Likely issue area:** PA scoping.
3. **Technical notes:** AUT-005; validate rendering_NPI at intake.
4. **Next debugging step:** Validate rendering_NPI against PA record at intake.

---

**Keywords:** authorization, wrong provider, PA transfer, rendering NPI, PA reissue

---

### RJ-044 – PA Issued for Different Facility
**Code:** AUT-006  
**CARC:** 15 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Wrong Facility

**Scenario:**  
PA approved for one hospital; service performed at another.

---

**Patient Explanation**

1. **What happened:** The approval was for a different facility.
2. **What it means for you:** A new facility-level approval is needed.
3. **What you should do next:** Your provider's office will handle this.

---

**Provider Action**

1. **Likely cause:** Facility-specific PA not honored at alternate location.
2. **What to verify:** Compare PA facility vs service facility.
3. **Next action:** Submit PA for actual facility or appeal.

---

**Analyst Notes**

1. **Interpretation:** Facility-PA mismatch.
2. **Likely issue area:** PA scoping.
3. **Technical notes:** AUT-006; require facility validation.
4. **Next debugging step:** Require facility validation prior to service if PA is facility-specific.

---

**Keywords:** authorization, wrong facility, facility-specific PA, PA reissue, appeal

---

### RJ-045 – Required Referral Not on File
**Code:** AUT-007  
**CARC:** 288 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Referral Missing

**Scenario:**  
Specialist visit under HMO with no PCP referral submitted.

---

**Patient Explanation**

1. **What happened:** Your HMO plan needs a referral from your primary doctor.
2. **What it means for you:** Without it, the visit isn't covered.
3. **What you should do next:** Get a referral from your PCP and we'll process it.

---

**Provider Action**

1. **Likely cause:** Referral required under HMO product.
2. **What to verify:** Confirm PCP referral document.
3. **Next action:** Obtain retro-referral if PCP supports.

---

**Analyst Notes**

1. **Interpretation:** Referral absence on HMO claim.
2. **Likely issue area:** Referral rules.
3. **Technical notes:** AUT-007; mandatory referral check at intake.
4. **Next debugging step:** Make referral-on-file check mandatory at intake for HMO products.

---

**Keywords:** authorization, referral, HMO, PCP, specialist

---

### RJ-046 – Referral Expired
**Code:** AUT-008  
**CARC:** 287 (Verify; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Referral Expired

**Scenario:**  
Referral valid for 90 days; specialist visit occurred 120 days later.

---

**Patient Explanation**

1. **What happened:** Your referral expired before the visit.
2. **What it means for you:** A new referral is needed.
3. **What you should do next:** Ask your primary doctor for a new one.

---

**Provider Action**

1. **Likely cause:** Referral past validity window.
2. **What to verify:** Verify referral start/end dates.
3. **Next action:** Obtain new referral and resubmit.

---

**Analyst Notes**

1. **Interpretation:** Referral expiry: elapsed=120d, valid=90d.
2. **Likely issue area:** Referral lifecycle.
3. **Technical notes:** AUT-008; surface expiry alerts.
4. **Next debugging step:** Add referral-expiry alerts to portals.

---

**Keywords:** authorization, expired referral, PCP, validity window, renewal

---

### RJ-047 – PA Denied — Lack of Medical Necessity
**Code:** AUT-009  
**CARC:** 50 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Medical Necessity

**Scenario:**  
PA for bariatric surgery denied; provider proceeded and billed anyway.

---

**Patient Explanation**

1. **What happened:** Your insurance found this procedure wasn't medically necessary.
2. **What it means for you:** There's an appeals process you can pursue.
3. **What you should do next:** Your doctor can file an appeal with more documentation.

---

**Provider Action**

1. **Likely cause:** Service performed after PA denial.
2. **What to verify:** Pull denial rationale and clinical documentation.
3. **Next action:** Initiate peer-to-peer or formal appeal.

---

**Analyst Notes**

1. **Interpretation:** Post-denial service event.
2. **Likely issue area:** Medical-necessity decisions.
3. **Technical notes:** AUT-009; trend high-risk CPTs after denial.
4. **Next debugging step:** Flag CPTs where service proceeds after PA denial for trend analysis.

---

**Keywords:** authorization, medical necessity, appeal, peer-to-peer, PA denial

---

### RJ-048 – Inpatient Admission Not Notified
**Code:** AUT-010  
**CARC:** 210 (Confirmed; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Notification

**Scenario:**  
Emergency admission not reported to payer within 24 hours.

---

**Patient Explanation**

1. **What happened:** Your hospital stay wasn't reported in time.
2. **What it means for you:** The hospital can submit late notification.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Notification SLA breach.
2. **What to verify:** Confirm admission timestamp and SLA window.
3. **Next action:** Submit late notification with reason; expect penalty.

---

**Analyst Notes**

1. **Interpretation:** Notification SLA breach.
2. **Likely issue area:** Inpatient notification rules.
3. **Technical notes:** AUT-010; integrate ADT feeds.
4. **Next debugging step:** Integrate ADT feeds to auto-notify payer on admission.

---

**Keywords:** authorization, notification, inpatient, ADT, SLA

---

### RJ-049 – Step Therapy Not Followed
**Code:** AUT-011  
**CARC:** B8 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Step Therapy

**Scenario:**  
High-cost biologic prescribed without trial of required first-line therapy.

---

**Patient Explanation**

1. **What happened:** Your plan requires trying a less expensive medication first.
2. **What it means for you:** Without that, the new one isn't approved.
3. **What you should do next:** Your doctor can show you've tried it or request an exception.

---

**Provider Action**

1. **Likely cause:** Step-therapy gate not passed.
2. **What to verify:** Confirm trial/failure of first-line agents.
3. **Next action:** Document trial or submit exception with justification.

---

**Analyst Notes**

1. **Interpretation:** Step-therapy gate not passed.
2. **Likely issue area:** Pharmacy formulary management.
3. **Technical notes:** AUT-011; expose step-therapy in e-prescribe.
4. **Next debugging step:** Surface step-therapy requirements in e-prescribe flow.

---

**Keywords:** authorization, step therapy, biologic, formulary, exception

---

### RJ-050 – Service Flagged Experimental
**Code:** AUT-012  
**CARC:** 55 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Experimental

**Scenario:**  
Gene therapy billed; payer policy classifies it as investigational without trial enrolment.

---

**Patient Explanation**

1. **What happened:** Your insurance considers this treatment experimental.
2. **What it means for you:** It isn't covered under standard benefits.
3. **What you should do next:** An appeal or clinical-trial pathway may be options.

---

**Provider Action**

1. **Likely cause:** Service classified investigational per payer policy.
2. **What to verify:** Pull current payer medical policy and any trial enrolment.
3. **Next action:** Route to appeals with peer-reviewed evidence.

---

**Analyst Notes**

1. **Interpretation:** Investigational-list hit.
2. **Likely issue area:** Experimental / investigational policy.
3. **Technical notes:** AUT-012; refresh investigational list from payer policies.
4. **Next debugging step:** Refresh investigational CPT list from payer medical policies.

---

**Keywords:** authorization, experimental, investigational, appeal, clinical trial

---
