# Rejection Code Mapping

> **Disclaimer:** independent personal project. No PHI, no PII, and no Medicaid, agency, or other non-public data is used. Only public reference information and synthetic (invented) examples. See the full disclaimer in the [README](../README.md#disclaimer).

Each scenario's legacy code (ELG/COD/PRV/AUT, invented for this project) is mapped to the real **Claim Adjustment Reason Code (CARC)** a payer would send on an 835 remittance. The "Meaning" column is our own plain-language summary, not the official wording. Official CARC descriptions are maintained and copyrighted by X12; see the [X12 CARC list](https://x12.org/codes/claim-adjustment-reason-codes).

Machine-readable version: [`data/reference/carc_mapping.csv`](../data/reference/carc_mapping.csv)

Status: **Confirmed** = checked against the X12 list or a published payer/CMS source · **Verify** = best fit, still to confirm · **Dropped** = not used in v1. **RARC** = Remittance Advice Remark Code, the extra detail sent with general codes like 16.

| Scenario | Legacy code | CARC | RARC | Meaning (our words) | Payer scope | Status | Note | Source |
|---|---|---|---|---|---|---|---|---|
| RJ-001 Policy lapsed on date of service | ELG-001 | 200 |  | Service fell in a gap when coverage had lapsed | all | Confirmed | Changed from 27 after checking the full list | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-002 Service before policy effective date | ELG-002 | 26 |  | Service happened before coverage started | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-003 Member ID not found | ELG-003 | 31 |  | Payer cannot match the patient to a member | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-004 Dependent exceeds age limit | ELG-004 | 32 |  | Patient is not an eligible dependent on this plan | commercial | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-005 Annual benefit maximum reached | ELG-005 | 119 |  | Benefit limit for the period has been used up | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-006 Service within waiting period | ELG-006 | 179 |  | Plan waiting period not yet met | commercial | Confirmed | Commercial only; not a Medicaid scenario | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-007 Service excluded under plan | ELG-007 | 204 |  | Service is not a covered benefit on this plan | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-008 Coverage ended with employment | ELG-008 | 27 |  | Service happened after coverage ended | commercial | Confirmed | Commercial only | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-009 Multiple primary policies (COB) | ELG-009 | 22 |  | Another payer should pay first (coordination of benefits) | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-010 Pre-existing condition exclusion | ELG-010 | 51 |  | Pre-existing condition not covered | commercial | Dropped (not used in v1) | Dropped: largely barred under the ACA |  |
| RJ-011 Service outside coverage territory | ELG-011 | 158 |  | Service was given outside the United States | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-012 Service not in plan tier | ELG-012 | 204 |  | Service is not a covered benefit on this plan | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-013 Coverage retroactively cancelled | ELG-013 | 27 |  | Service happened after coverage ended | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-014 ICD-10 code lacks specificity | COD-001 | 146 |  | Diagnosis code not valid for the date of service | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-015 Procedure inconsistent with diagnosis | COD-002 | 11 |  | Diagnosis does not support the procedure | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-016 Unbundling | COD-003 | 236 |  | Procedure not allowed with another same-day procedure per NCCI | all | Confirmed | 97 is the alternative | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-017 E&M level not supported (upcoding) | COD-004 | 150 |  | Documentation does not support this level of service | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-018 Missing or invalid modifier | COD-005 | 4 |  | Procedure code does not fit the modifier used | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-019 Procedure conflicts with patient sex | COD-006 | 7 |  | Procedure does not fit the patient's recorded sex | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-020 Procedure conflicts with patient age | COD-007 | 6 |  | Procedure does not fit the patient's age | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-021 Mutually exclusive procedures | COD-008 | 231 |  | Two procedures cannot be billed together the same day | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-022 Diagnosis code missing | COD-009 | 16 | M76 | Claim is missing information or has a billing error | all | Confirmed | Remark code says the diagnosis is missing or invalid | [link](https://med.noridianmedicare.com/web/jddme/topics/ra/denial-resolution/m76-16) |
| RJ-023 Frequency limit exceeded | COD-010 | 151 |  | Too many units or too frequent for what was documented | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-024 Invalid NDC | COD-011 | 16 | M119 | Claim is missing information or has a billing error | all | Confirmed | Remark code says the NDC is missing, invalid, deactivated or withdrawn | [link](https://med.noridianmedicare.com/web/jadme/topics/ra/denial-resolution/m119-16) |
| RJ-025 Place of service mismatch | COD-012 | 5 |  | Procedure does not fit the place of service | all | Confirmed | 58 is the alternative | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-026 Wrong revenue code for facility | COD-013 | 282 |  | Code does not fit the type of bill | all | Confirmed | 199 if revenue and procedure codes don't match | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-027 Out of network without referral | PRV-001 | 242 |  | Service not from a network or primary care provider | all | Confirmed | 288 if the main issue is the missing referral | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-028 Provider license expired | PRV-002 | B7 |  | Provider was not eligible to be paid on this date | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-029 Invalid or inactive NPI | PRV-003 | 208 | N290 | NPI on the claim could not be matched | all | Confirmed | CARC 208 = NPI not matched; N290 for the rendering NPI, N257 if it's the billing NPI | [link](https://med.noridianmedicare.com/web/jfb/topics/claim-submission/reason-code-guidance/missing-incorrect-req-npi-info) |
| RJ-030 Provider not credentialed | PRV-004 | B7 |  | Provider was not eligible to be paid on this date | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-031 Service outside provider specialty | PRV-005 | 8 |  | Procedure does not fit the provider's specialty/taxonomy | all | Confirmed | 185 is the alternative | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-032 Invalid taxonomy code | PRV-006 | 16 | N288 | Claim is missing information or has a billing error | all | Confirmed | N288 = rendering provider taxonomy; use N255 if it's the billing provider's taxonomy | [link](https://medicaid.ncdhhs.gov/blog/2021/08/27/claims-denied-taxonomy-codes-missing-incorrect-or-inactive) |
| RJ-033 Provider on exclusion list | PRV-007 | B7 |  | Provider was not eligible to be paid on this date | all | Confirmed | B7 confirmed on X12 list; no single remark code for OIG exclusion confirmed | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-034 Missing provider signature | PRV-008 | 16 | MA81 | Claim is missing information or has a billing error | all | Verify | MA81 (provider/supplier signature) found only on secondary sites; confirm against X12 | [link](https://www.mdclarity.com/denial-code-rarc/ma81) |
| RJ-035 Facility not enrolled | PRV-009 | B7 |  | Provider was not eligible to be paid on this date | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-036 TIN/NPI mismatch | PRV-010 | 16 | N209 | Claim is missing information or has a billing error | all | Confirmed | N209 = missing/incomplete/invalid taxpayer ID (TIN) | [link](https://www.dmas.virginia.gov/media/2140/npi-related-error-codes-resolutions-for-cms-1500-08-05.pdf) |
| RJ-037 Supervising provider missing | PRV-011 | 16 | N297 | Claim is missing information or has a billing error | all | Verify | N297 = supervising provider primary identifier (N296 for the name); found only on secondary sites | [link](https://www.codingahead.com/remark-code-m506/) |
| RJ-038 Service address mismatch | PRV-012 | 16 | N294 | Claim is missing information or has a billing error | all | Confirmed | N294 = service facility address; MA114 is the alternative (where services were furnished) | [link](https://medicare.fcso.com/claims/tips-prevent-ruc-co-16) |
| RJ-039 Prior authorization missing | AUT-001 | 197 |  | Required authorization or notification was not obtained | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-040 Prior authorization expired | AUT-002 | 302 |  | Authorization time limit had passed | all | Confirmed | 302 confirmed on X12 list: authorization time limit expired | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-041 Auth for a different procedure | AUT-003 | 284 |  | Auth exists but does not cover the billed service | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-042 Auth units exceeded | AUT-004 | 198 |  | Billed more than the authorization allowed | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-043 Auth for a different provider | AUT-005 | 296 |  | Auth exists but does not cover this provider | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-044 Auth for a different facility | AUT-006 | 296 |  | Auth exists but does not cover this provider or facility | all | Verify | Was 15, but X12 deactivated 15 on 05/01/2018. 296 (auth doesn't apply to the provider) is the best fit since a facility is a provider | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-045 Referral missing | AUT-007 | 288 |  | Required referral is absent | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-046 Referral expired | AUT-008 | 287 |  | Referral limit exceeded | all | Confirmed | 287 (referral exceeded) confirmed; no CARC specifically for an expired referral, so this is the closest | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-047 Not medically necessary | AUT-009 | 50 |  | Payer judged the service not medically necessary | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-048 Admission notice late | AUT-010 | 210 |  | Authorization or notice was not received in time | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-049 Step therapy not followed | AUT-011 | B8 |  | A cheaper alternative should have been tried first | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
| RJ-050 Experimental treatment | AUT-012 | 55 |  | Payer considers the service experimental | all | Confirmed |  | [link](https://x12.org/codes/claim-adjustment-reason-codes) |
