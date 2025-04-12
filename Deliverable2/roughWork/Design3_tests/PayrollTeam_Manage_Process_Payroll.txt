User Story:
As an Payroll Staff Member, I want to process payroll for the month so that employees can receive their monthly salary, 
including any applicable deductions or bonuses

Feature:
Payroll Staff Member Manages and Processes payroll

Feature should enable Payroll Staff Member to process payroll for all employees, calculate any deductions,
bonuses and mark the payroll as "Processed"

Scenario 1: Payroll Staff Member Processes Payroll for the month
Given the Payroll Staff Member is logged in
When the Payroll Staff Member selects "Process Payroll for the month"
Then the payroll should be calculated for all the employees,
including deductions, bonuses and mark the payroll as "Processed"

Test Design:
Step 1: Login to the system with Payroll Staff Member credentials
Step 2: Select "Process Payroll for the month" 
Step 3: The system calculates employees salaries, deductions and bonuses for the month
Step 4: Mark the payroll as "Processed" once the calculation is complete

Expected Outcome:
Payroll is calculated for all employees, with deductions and bonuses
The Payroll is marked as "Processed" and employees are notified about their payslips or something