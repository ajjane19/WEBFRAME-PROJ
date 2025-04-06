User Story:
As an HR staff member, I want to manage and process payroll for employees 
so that I can ensure employees are paid accurately.

Feature:
HR Manages payroll

Feature allows HR staff to manage and process employee payroll

Scenario 1: HR processes payroll employees
Given the HR Staff is logged in
When the HR Staff selects "Process Payroll"
Then the payroll should be processed and employees should recieve their payslips

Scenario 2: HR reviews payroll history
Given the HR staff is logged in
When the HR staff selects "View Payroll History"
Then the HR staff should see a list of past payroll with detailed employee payments

Test Design:
Step 1: Login to the system with valid HR credentials
Step 2: select "Process Payroll" to process the payroll for employees
Step 3: The system processes the payroll and generates payslips for employees

Expected Outcome:
Employees payroll is processed and they receive their payslips
A list of past payrolls with detailed employee payments is displayed