User Story:
As a Team Leader, I want to monitor campaign progress
Ensuring the campaigns are on track and meet performance targets

Feature:
Team Leader Monitors Campaign Progress

Feature should enable Team Leader to monitor the status and progress of each Campaign

Scenario: Team Leader Monitors campaign Progress
Given the Team Leader is logged in
When the Team Leader accesses the "Campaign Progress"
Then it should show the Team Leader should see a summary of ongoing campaigns and their statuses.

Scenario 2: Team Leader ensures campaigns are on track
Given the Team Leader is monitoring a campaign
When the Team Leader reviews the campaign metrics
Then the Team Leader should ensure the campaign is meeting performance targets and deadlines


Test Design:
Step 1: Login to the system with Team Leader credentials
Step 2: Navigate to campaigns
Step 3: System should display the details of campaign
Step 4: The Team Leader reviews the campaign metrics and checks if the campaign is meeting performance targets.

Expected Outcome:
Team Leader should be able to view summary of campaigns with their stats
Being able to ensure each campaign is on track by review it's performance