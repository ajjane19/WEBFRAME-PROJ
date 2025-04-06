User Story:
As a Supervisor, I want to assign employees to campaigns so that
they can contribute to campaigns.

Feature:
Supervisor assigns Employees to campaigns

Feature should allow Superviso to assign employees to campaigns

Scenario 1: Supervisor Assigns Employees to a Campaign
Given the Supervisor is logged in
When the Supervisor selects a campaign and assigns employees to its
Then employees should be added to the campaign

Test Design:
Step 1: Login to the system with Supervisor credentials
Step 2: Select a campaign from the list
Step 3: Assign employees to the selected campaign

Expected Outcome:
Employees are successfully added to the campaign
The supervisor can see a list of employees assigned to the campaign
