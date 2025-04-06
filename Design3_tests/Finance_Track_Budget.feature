User Story:
As a Finanace Team Member, I want to track the budget for campaigns 
so that I can monitor if the campaign is within the budget.

Feature: 
Finance Tracks budget

Feature should allow the finance team to track the budget status of campaigns

Scenario: Finance tracks the budget for a campaign
Given the finance team member is logged in
When the finance team member accesses the "campaign budget"
Then the finance team member should see the current budget

Test Design:
Step 1: Login to the system with valid finance credentials
Step 2: Navigate to the Campaign budget
Step 3: The system retrieves and displays the current budget status for the campaign

Expected Outcome:
The finance team member sees the current budget status along with any planned budget.