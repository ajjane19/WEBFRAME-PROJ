User Story:
As a Manager, I want to generate campaign reports so that I can assess the campaign's 
performance, budget and those involved.

Feature:
Manager generates Campaign reports

Feature allows Manager to generate detailed campaign reports, 
including perfomance, budget and those involved. 
Being able to pick a campaign and view its history and report

Scenario 1: Manager generates a camp
Given the Manager is logged in
When Manager selects Campaign and clicks Generate reports
Then Manager should receive a detailed campaign report 
including performance, budget and those involved.

Scenario 2: Manager reviews Campaign
Given the Manager has access to multiple campaigns
When the Manager selects "View Campaign History"
Then Manager should have access to view all campaigns with their report

Test Design:
Step 1: Login to the system with Manager credentials
Step 2: Select a campaign from list
Step 3: Click Generate report
Step 4: Report should include perfomance, budget and those involved
Step 5: If the manager clicks "View Campaign History" a list of all campaigns with their report should show up

Expected Outcome:
A detailed campaign report should be generated with relevant data.
The Manager can view a list of all campaigns and their reports.
