# Rejection Code Mapping

> **Disclaimer:** independent personal project. No PHI, no PII, and no Medicaid, agency, or other non-public data is used. Only public reference information and synthetic (invented) examples. See the full disclaimer in the [README](../README.md#disclaimer).

Each scenario's legacy code (ELG/COD/PRV/AUT, invented for this project) is mapped to the real **Claim Adjustment Reason Code (CARC)** a payer would send on an 835 remittance. The "Meaning" column is our own plain-language summary, not the official wording. Official CARC descriptions are maintained and copyrighted by X12; see the [X12 CARC list](https://x12.org/codes/claim-adjustment-reason-codes).

Machine-readable version: [`data/reference/carc_mapping.csv`](../data/reference/carc_mapping.csv)

Status: **Confirmed** = checked against the X12 list · **Verify** = best fit, still to confirm · **Needs RARC** = CARC 16 is generic and needs a Remittance Advice Remark Code to say what's wrong · **Dropped** = not used in v1.

| Scenario | Legacy code | CARC | Meaning (our words) | Payer scope | Status | Note |
|---|---|---|---|---|---|---|
| RJ-001 Policy lapsed on date of service | ELG-001 | 200 | Service fell in a gap when coverage had lapsed | all | Confirmed | Changed from 27 after checking the full list |
| RJ-002 Service before policy effective date | ELG-002 | 26 | Service happened before coverage started | all | Confirmed |  |
| RJ-003 Member ID not found | ELG-003 | 31 | Payer cannot match the patient to a member | all | Confirmed |  |
| RJ-004 Dependent exceeds age limit | ELG-004 | 32 | Patient is not an eligible dependent on this plan | commercial | Confirmed |  |
| RJ-005 Annual benefit maximum reached | ELG-005 | 119 | Benefit limit for the period has been used up | all | Confirmed |  |
| RJ-006 Service within waiting period | ELG-006 | 179 | Plan waiting period not yet met | commercial | Confirmed | Commercial only; not a Medicaid scenario |
| RJ-007 Service excluded under plan | ELG-007 | 204 | Service is not a covered benefit on this plan | all | Confirmed |  |
| RJ-008 Coverage ended with employment | ELG-008 | 27 | Service happened after coverage ended | commercial | Confirmed | Commercial only |
| RJ-009 Multiple primary policies (COB) | ELG-009 | 22 | Another payer should pay first (coordination of benefits) | all | Confirmed |  |
| RJ-010 Pre-existing condition exclusion | ELG-010 | 51 | Pre-existing condition not covered | commercial | Dropped (not used in v1) | Dropped: largely barred under the ACA |
| RJ-011 Service outside coverage territory | ELG-011 | 158 | Service was given outside the United States | all | Confirmed |  |
| RJ-012 Service not in plan tier | ELG-012 | 204 | Service is not a covered benefit on this plan | all | Confirmed |  |
| RJ-013 Coverage retroactively cancelled | ELG-013 | 27 | Service happened after coverage ended | all | Confirmed |  |
| RJ-014 ICD-10 code lacks specificity | COD-001 | 146 | Diagnosis code not valid for the date of service | all | Confirmed |  |
| RJ-015 Procedure inconsistent with diagnosis | COD-002 | 11 | Diagnosis does not support the procedure | all | Confirmed |  |
| RJ-016 Unbundling | COD-003 | 236 | Procedure not allowed with another same-day procedure per NCCI | all | Confirmed | 97 is the alternative |
| RJ-017 E&M level not supported (upcoding) | COD-004 | 150 | Documentation does not support this level of service | all | Confirmed |  |
| RJ-018 Missing or invalid modifier | COD-005 | 4 | Procedure code does not fit the modifier used | all | Confirmed |  |
| RJ-019 Procedure conflicts with patient sex | COD-006 | 7 | Procedure does not fit the patient's recorded sex | all | Confirmed |  |
| RJ-020 Procedure conflicts with patient age | COD-007 | 6 | Procedure does not fit the patient's age | all | Confirmed |  |
| RJ-021 Mutually exclusive procedures | COD-008 | 231 | Two procedures cannot be billed together the same day | all | Confirmed |  |
| RJ-022 Diagnosis code missing | COD-009 | 16 | Claim is missing information or has a billing error | all | Needs RARC | Needs a remark code (RARC) to say what is missing |
| RJ-023 Frequency limit exceeded | COD-010 | 151 | Too many units or too frequent for what was documented | all | Confirmed |  |
| RJ-024 Invalid NDC | COD-011 | 16 | Claim is missing information or has a billing error | all | Needs RARC | Needs a remark code (RARC) |
| RJ-025 Place of service mismatch | COD-012 | 5 | Procedure does not fit the place of service | all | Confirmed | 58 is the alternative |
| RJ-026 Wrong revenue code for facility | COD-013 | 282 | Code does not fit the type of bill | all | Confirmed | 199 if revenue and procedure codes don't match |
| RJ-027 Out of network without referral | PRV-001 | 242 | Service not from a network or primary care provider | all | Confirmed | 288 if the main issue is the missing referral |
| RJ-028 Provider license expired | PRV-002 | B7 | Provider was not eligible to be paid on this date | all | Confirmed |  |
| RJ-029 Invalid or inactive NPI | PRV-003 | 208 | NPI on the claim could not be matched | all | Verify | B7 is the alternative |
| RJ-030 Provider not credentialed | PRV-004 | B7 | Provider was not eligible to be paid on this date | all | Confirmed |  |
| RJ-031 Service outside provider specialty | PRV-005 | 8 | Procedure does not fit the provider's specialty/taxonomy | all | Confirmed | 185 is the alternative |
| RJ-032 Invalid taxonomy code | PRV-006 | 16 | Claim is missing information or has a billing error | all | Needs RARC | Needs a remark code (RARC) |
| RJ-033 Provider on exclusion list | PRV-007 | B7 | Provider was not eligible to be paid on this date | all | Verify | Confirm with a remark code |
| RJ-034 Missing provider signature | PRV-008 | 16 | Claim is missing information or has a billing error | all | Needs RARC | Needs a remark code (RARC) |
| RJ-035 Facility not enrolled | PRV-009 | B7 | Provider was not eligible to be paid on this date | all | Confirmed |  |
| RJ-036 TIN/NPI mismatch | PRV-010 | 16 | Claim is missing information or has a billing error | all | Needs RARC | Needs a remark code (RARC) |
| RJ-037 Supervising provider missing | PRV-011 | 16 | Claim is missing information or has a billing error | all | Needs RARC | Needs a remark code (RARC) |
| RJ-038 Service address mismatch | PRV-012 | 16 | Claim is missing information or has a billing error | all | Needs RARC | Needs a remark code (RARC) |
| RJ-039 Prior authorization missing | AUT-001 | 197 | Required authorization or notification was not obtained | all | Confirmed |  |
| RJ-040 Prior authorization expired | AUT-002 | 302 | Authorization time limit had passed | all | Verify | 197 is the alternative |
| RJ-041 Auth for a different procedure | AUT-003 | 284 | Auth exists but does not cover the billed service | all | Confirmed |  |
| RJ-042 Auth units exceeded | AUT-004 | 198 | Billed more than the authorization allowed | all | Confirmed |  |
| RJ-043 Auth for a different provider | AUT-005 | 296 | Auth exists but does not cover this provider | all | Confirmed |  |
| RJ-044 Auth for a different facility | AUT-006 | 15 | Auth number missing invalid or not for this service/provider | all | Confirmed |  |
| RJ-045 Referral missing | AUT-007 | 288 | Required referral is absent | all | Confirmed |  |
| RJ-046 Referral expired | AUT-008 | 287 | Referral limit exceeded | all | Verify | Check whether 287 fits an expired referral |
| RJ-047 Not medically necessary | AUT-009 | 50 | Payer judged the service not medically necessary | all | Confirmed |  |
| RJ-048 Admission notice late | AUT-010 | 210 | Authorization or notice was not received in time | all | Confirmed |  |
| RJ-049 Step therapy not followed | AUT-011 | B8 | A cheaper alternative should have been tried first | all | Confirmed |  |
| RJ-050 Experimental treatment | AUT-012 | 55 | Payer considers the service experimental | all | Confirmed |  |
