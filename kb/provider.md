# Provider Rejections

AI knowledge base — provider rejections scenarios optimized for RAG retrieval.

---

### RJ-027 – Out-of-Network Without Referral
**Code:** PRV-001  
**CARC:** 242 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Network Status

**Scenario:**  
HMO member visited a non-contracted specialist without a PCP referral.

---

**Patient Explanation**

1. **What happened:** The specialist isn't in your plan's network and you didn't have a referral.
2. **What it means for you:** Coverage is limited or denied under HMO rules.
3. **What you should do next:** Get a referral from your primary doctor next time.

---

**Provider Action**

1. **Likely cause:** OON specialist + missing HMO referral.
2. **What to verify:** Confirm network status and referral on file.
3. **Next action:** Apply OON benefit or deny per plan rules.

---

**Analyst Notes**

1. **Interpretation:** Network + referral double-miss.
2. **Likely issue area:** Network / referral rules.
3. **Technical notes:** PRV-001; HMO product gating.
4. **Next debugging step:** Surface referral-required flag in member portal.

---

**Keywords:** provider, out of network, OON, HMO, PCP referral

---

### RJ-028 – Expired Provider License
**Code:** PRV-002  
**CARC:** B7 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** License Issue

**Scenario:**  
Rendering provider's license expired 60 days before service date.

---

**Patient Explanation**

1. **What happened:** There's an issue with the provider's records — not your care.
2. **What it means for you:** We're working with the provider's office to resolve it.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Provider license inactive on DOS.
2. **What to verify:** Verify license status with state board.
3. **Next action:** Escalate to credentialing; reconsider after renewal.

---

**Analyst Notes**

1. **Interpretation:** License invalid on DOS.
2. **Likely issue area:** Credentialing / licensure.
3. **Technical notes:** PRV-002; sync license status from state boards.
4. **Next debugging step:** Auto-sync license status from state boards.

---

**Keywords:** provider, license expired, credentialing, state board, licensure

---

### RJ-029 – Inactive NPI
**Code:** PRV-003  
**CARC:** 208 (Verify; payer scope: all)  
**Severity:** High  
**Sub-Category:** NPI Invalid

**Scenario:**  
NPI submitted is deactivated per NPPES registry.

---

**Patient Explanation**

1. **What happened:** A provider identifier on the claim is no longer active.
2. **What it means for you:** The provider's billing team will fix this.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** NPI deactivated in NPPES.
2. **What to verify:** Confirm current active NPI.
3. **Next action:** Resubmit with valid NPI.

---

**Analyst Notes**

1. **Interpretation:** NPI deactivation flag.
2. **Likely issue area:** Provider identifiers.
3. **Technical notes:** PRV-003; integrate NPPES daily refresh.
4. **Next debugging step:** Integrate NPPES API for daily NPI status refresh.

---

**Keywords:** provider, NPI, NPPES, identifier, deactivated

---

### RJ-030 – Provider Not Credentialed
**Code:** PRV-004  
**CARC:** B7 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Credentialing

**Scenario:**  
New physician billed before credentialing completion date.

---

**Patient Explanation**

1. **What happened:** The doctor's paperwork with your insurer isn't done yet.
2. **What it means for you:** The office will resubmit once it's complete.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Credentialing not yet effective.
2. **What to verify:** Confirm credentialing effective date.
3. **Next action:** Hold claims until effective date; consider retro-effective if allowed.

---

**Analyst Notes**

1. **Interpretation:** Credentialing gap.
2. **Likely issue area:** Provider enrollment.
3. **Technical notes:** PRV-004; auto-hold queue.
4. **Next debugging step:** Auto-hold claims until credentialing_complete_date.

---

**Keywords:** provider, credentialing, enrollment, effective date, billing hold

---

### RJ-031 – Service Outside Specialty
**Code:** PRV-005  
**CARC:** 8 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Specialty Mismatch

**Scenario:**  
GP billed a complex neurosurgical procedure.

---

**Patient Explanation**

1. **What happened:** The procedure doesn't match the provider's usual specialty.
2. **What it means for you:** We're reviewing with the provider.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Scope-of-practice mismatch.
2. **What to verify:** Confirm rendering provider and credentials.
3. **Next action:** Reroute to scope-of-practice review.

---

**Analyst Notes**

1. **Interpretation:** Specialty-CPT mismatch.
2. **Likely issue area:** Specialty / scope-of-practice.
3. **Technical notes:** PRV-005; escalate repeat occurrences.
4. **Next debugging step:** Add specialty-scope validator; flag for fraud review on repeats.

---

**Keywords:** provider, specialty mismatch, scope of practice, credentialing, audit

---

### RJ-032 – Invalid Taxonomy Code
**Code:** PRV-006  
**CARC:** 16 (Needs RARC; payer scope: all)  
**Severity:** Low  
**Sub-Category:** Taxonomy

**Scenario:**  
Submitted taxonomy doesn't match provider's registered specialty.

---

**Patient Explanation**

1. **What happened:** A small record-keeping mismatch is delaying the claim.
2. **What it means for you:** The billing team will fix it.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Taxonomy doesn't match enrollment file.
2. **What to verify:** Compare claim taxonomy vs enrollment record.
3. **Next action:** Update claim or enrollment record.

---

**Analyst Notes**

1. **Interpretation:** Taxonomy vs enrollment mismatch.
2. **Likely issue area:** Provider enrollment data.
3. **Technical notes:** PRV-006; sync enrollment with claim feed.
4. **Next debugging step:** Sync enrollment data with claim feed.

---

**Keywords:** provider, taxonomy, enrollment, specialty code, data sync

---

### RJ-033 – Provider on Exclusion List
**Code:** PRV-007  
**CARC:** B7 (Verify; payer scope: all)  
**Severity:** High  
**Sub-Category:** Sanctioned Provider

**Scenario:**  
Rendering provider appears on OIG LEIE exclusion list.

---

**Patient Explanation**

1. **What happened:** There's a compliance issue with the provider on this claim.
2. **What it means for you:** We're handling it internally.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Provider on OIG LEIE exclusion.
2. **What to verify:** Verify match against latest LEIE/SAM data.
3. **Next action:** Do not pay; escalate to SIU/compliance.

---

**Analyst Notes**

1. **Interpretation:** LEIE match.
2. **Likely issue area:** Compliance / sanctions.
3. **Technical notes:** PRV-007; cross-check OIG/SAM monthly.
4. **Next debugging step:** Cross-check all claims against OIG/SAM monthly.

---

**Keywords:** provider, OIG, LEIE, sanction, exclusion list

---

### RJ-034 – Missing Provider Signature
**Code:** PRV-008  
**CARC:** 16 (Needs RARC; payer scope: all)  
**Severity:** Low  
**Sub-Category:** Missing Signature

**Scenario:**  
Paper claim submitted without rendering provider signature.

---

**Patient Explanation**

1. **What happened:** A signature is missing from your paper claim.
2. **What it means for you:** The provider will resign and resubmit.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Paper-form completeness issue.
2. **What to verify:** Confirm signature requirement on form.
3. **Next action:** Obtain signature and resubmit; promote EDI.

---

**Analyst Notes**

1. **Interpretation:** Form-completeness failure.
2. **Likely issue area:** Paper-claim handling.
3. **Technical notes:** PRV-008; promote EDI submissions.
4. **Next debugging step:** Promote EDI submissions to eliminate signature gaps.

---

**Keywords:** provider, signature, paper claim, EDI, form completeness

---

### RJ-035 – Facility Not Enrolled
**Code:** PRV-009  
**CARC:** B7 (Confirmed; payer scope: all)  
**Severity:** High  
**Sub-Category:** Facility Not Enrolled

**Scenario:**  
Surgical center not contracted or enrolled with the payer network.

---

**Patient Explanation**

1. **What happened:** The facility you used isn't enrolled with your insurer.
2. **What it means for you:** Coverage may be limited or denied.
3. **What you should do next:** Ask your provider about in-network options.

---

**Provider Action**

1. **Likely cause:** Facility absent from enrolled-provider file.
2. **What to verify:** Verify facility enrollment status.
3. **Next action:** Escalate to network-management or redirect future services.

---

**Analyst Notes**

1. **Interpretation:** Facility not in enrolled-provider file.
2. **Likely issue area:** Network enrollment.
3. **Technical notes:** PRV-009; route to network management.
4. **Next debugging step:** Escalate to network-management for enrollment follow-up.

---

**Keywords:** provider, facility, enrollment, network management, ASC

---

### RJ-036 – TIN Doesn't Match NPI
**Code:** PRV-010  
**CARC:** 16 (Needs RARC; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Tax ID Mismatch

**Scenario:**  
Submitted TIN doesn't match on-file TIN for the provider NPI.

---

**Patient Explanation**

1. **What happened:** A tax ID mismatch is delaying the claim.
2. **What it means for you:** The provider's office will update it.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** TIN/NPI link mismatch.
2. **What to verify:** Verify W-9 on file.
3. **Next action:** Update enrollment record with correct TIN/NPI.

---

**Analyst Notes**

1. **Interpretation:** TIN-NPI link mismatch.
2. **Likely issue area:** Provider enrollment data.
3. **Technical notes:** PRV-010; trigger W-9 verification.
4. **Next debugging step:** Trigger W-9 verification workflow.

---

**Keywords:** provider, tax ID, TIN, NPI, W-9

---

### RJ-037 – Missing Supervising Provider
**Code:** PRV-011  
**CARC:** 16 (Needs RARC; payer scope: all)  
**Severity:** Medium  
**Sub-Category:** Supervising Provider

**Scenario:**  
Resident services billed without supervising physician info.

---

**Patient Explanation**

1. **What happened:** A required supervising doctor's name is missing.
2. **What it means for you:** The provider will add it and resubmit.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Supervising NPI missing on resident-rendered service.
2. **What to verify:** Confirm supervising physician details.
3. **Next action:** Add supervising NPI and role indicator.

---

**Analyst Notes**

1. **Interpretation:** Mandatory field missing: supervising_NPI.
2. **Likely issue area:** Teaching-physician rules.
3. **Technical notes:** PRV-011; validate teaching-context fields.
4. **Next debugging step:** Validate teaching-context fields at intake.

---

**Keywords:** provider, supervising provider, resident, teaching physician, NPI

---

### RJ-038 – Service Location Address Mismatch
**Code:** PRV-012  
**CARC:** 16 (Needs RARC; payer scope: all)  
**Severity:** Low  
**Sub-Category:** Address Mismatch

**Scenario:**  
Service-facility address doesn't match any enrolled location for the NPI.

---

**Patient Explanation**

1. **What happened:** The service address doesn't match the provider's records.
2. **What it means for you:** The office will correct it.
3. **What you should do next:** No action needed from you.

---

**Provider Action**

1. **Likely cause:** Service location not matched to enrolled practice.
2. **What to verify:** Verify enrolled practice locations.
3. **Next action:** Update address or add new practice location.

---

**Analyst Notes**

1. **Interpretation:** Address-to-enrollment match failed.
2. **Likely issue area:** Provider enrollment data.
3. **Technical notes:** PRV-012; run address normalization + fuzzy match.
4. **Next debugging step:** Run address normalization and fuzzy match before rejection.

---

**Keywords:** provider, address, service location, enrollment, fuzzy match

---
