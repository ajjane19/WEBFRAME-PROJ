User Story: 
As a Manager, I want to review and approve employee entries 
before processsing payroll so that I can ensure the accuracy of the enteries

Feature: 
Manager Reviews and Approves Employee entries

Feature should enable the manager to review and 
approve employee entries before payroll processing

Scenario 1: Manager reviews employee entries
Given the manager is logged in
When the manager accesses the Employee Entries 
Then manager should be to view all employee entries

Scenario 2: Manager approves employee entries
Given the manager is reviewing employee entries
When manager selects an entry and clicks "Approve"
Then the employee entry should be marked as approved

Test Design:
Step 1: Login to the system with Manager credentials
Step 2: Access the "Employee Entries"
Step 3: Review all employee entries
Step 4: The manager selects entries to approve by clicking the "Approve" button
Step 5: The system should mark the selected enteries as approved

Expected Outcome:
All employee entries are displayed for review
The selected entries for approval should be marked as approved once button is clicked