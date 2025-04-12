User Story:
As a Manager, I want to assigns my employees to specific campaigns so that I can ensure
the right team is working on the campaign.

Feature:
Manager assigns their employees

Feature allows Manager to assign employees to a specific campaign, 
secelting the employees and designating their Team Leader for that campaign.
The system will notify the Manager about the employees assigned and provide relevant
details about campaign

Scenario 1: Manager assigns their employees
Given the Manager is logged in
When Manager selects Campaign and inputs employees and Team Leader name.
The system should notify the Manager that the employees have been assigned to the
campaign and it should include the names of employees and campaign

Test Design:
Step 1: Login to the system with Manager credentials
Step 2: Select a campaign from list
Step 3: assign employees and supervisor to the campaign
Step 4: Notify Manager of successful assignment

Expected Outcome:
Manager successfully assigns employes to the selected campaign.
Notfication is displayed and it should include the names of employees and campaign
