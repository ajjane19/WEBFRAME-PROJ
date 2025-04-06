User Story:
As a Supervisor, I want to monitor campaign progress
Ensuring the campaigns are on track and meet performance targets

Feature:
Supervisor Monitors Campaign Progress

Feature should enable Supervisor to monitor the status and progress of each Campaign

Scenario: Supervisor Monitors campaign Progress
Given the supervisor is logged in
When the supervisor accesses the "Campaign Progress"
Then it should show the supervisor should see a summary of ongoing campaigns and their statuses.

Scenario 2: Supervisor ensures campaigns are on track
Given the Supervisor is monitoring a campaign
When the Supervisor reviews the campaign metrics
Then the Supervisor should ensure the campaign is meeting performance targets and deadlines


Test Design:
Step 1: Login to the system with Supervisor credentials
Step 2: Navigate to campaigns
Step 3: System should display the details of campaign
Step 4: The supervisor reviews the campaign metrics and checks if the campaign is meeting performance targets.

Expected Outcome:
Supervisor should be able to view summary of campaigns with their stats
Being able to ensure each campaign is on track by review it's performance