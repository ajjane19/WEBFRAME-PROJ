User Story:
As an employee, I want to access my payslip
so I can view my salary, deductions and bonuses.

Feature:
Employee Payslip access

Feature enables employees to view their payslip salary, 
including deductions and bonuses

Scenario: 
Given the Employee is logged in
When the Employee navigates to the Payslip
Then Employee should be able to view their payslip with salary, deductions and bonus details

Test Design:
Step 1: Login to the system with Employee credentials
Step 2: Navigate to Payslip from Employee dashboard
Step 3: System should recieve Employee data
Step 4: Employee should be able to see their Payslip

Expected Outcome:
- Payslip is displayed with salary, deductions and bonuses