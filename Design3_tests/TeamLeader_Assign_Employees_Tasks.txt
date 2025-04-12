User Story:
As a Team Leader, I want to assign tasks to employees so that
they can contribute to campaigns effectively.

Feature:
Team Leader assigns tasks to employee

Feature should allow Team Leader to assign tasks to employee within a campaign.
Should allow the Team Leader to select employees and assign them tasks, ensuing the proper
distribution of work.

Scenario 1: Team Leader Assigns Employees to a Campaign
Given the Team Leader is logged in
When the Team Leader selects an employee and assigns a task to them
Then the task should be successfully assigned to teh employee 
and they should be notified of the task.

Test Design:
Step 1: Login to the system with Team Leader credentials
Step 2: Select an employee from the list
Step 3: Assign employees tasks
step 4: Notify employee of the task assigned

Expected Outcome:
Team Leader successfully assigns tasks to employees
Employee recieves a notification confirming the task assignment,
including the task descriptions and campaign.
