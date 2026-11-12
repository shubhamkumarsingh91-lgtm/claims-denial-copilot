# Week 2 Persona Testing

## Input
Claim rejected: Member not eligible on date of service

### Patient Translator

1. What happened  
The insurance company determined the patient’s coverage was not active on the date the service was provided.  

2. What it means for you  
Your claim was rejected because the insurance policy for the person receiving care was not valid on the day the service was done.  

3. What you should do next  
- Check the insurance policy dates to confirm coverage was active on the service date  
- Verify the member ID used matches the patient’s record  
- Contact the insurance company to confirm eligibility status

### Provider Translator

1. Likely cause: Eligibility failure due to coverage expiring or the service date falling outside active coverage.  
2. What to verify:  
   - Confirm the service date is within the patient's active coverage period.  
   - Verify the member ID matches the insured individual.  
   - Check if coverage was renewed or extended.  
3. Next action: Resubmit the claim with updated coverage details or contact the payer to confirm eligibility status.

### Analyst Translator

1. Interpretation: The claim was rejected due to eligibility failure, indicating the patient's insurance coverage was not active on the date of service.  
2. Likely issue area: Coverage expiration or incorrect member ID/eligibility status on the service date.  
3. Technical notes: Validate the service date against the member's coverage period and confirm the member ID matches the patient's record.  
4. Next debugging step: Check the service date against the payer's coverage effective dates and verify the member ID in the claim against the patient's enrollment record.
