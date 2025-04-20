from django.db import models

# Creating a manager model, which will be used to approve entries and manage campaigns
class Manager(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Creating a payroll team member model - used to represent users who process payslips after approval
class PayrollTeam(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Creating a Employee model - Regular users who clock in/out and view their payslip
class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
# Creating a Team Leader model - these users assign tasks to employees and monitor progress
class TeamLeader(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    employee_ref = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='as_team_leader')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # Getting all employees under certain team leader
    def get_team_member(self):
        return Employee.objects.filter(as_team_leader=self)

# Creating a campaigns model, projects that employees are assigned to
class Campaign(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    manager = models.ManyToManyField(Manager, related_name='campaigns')
    team_leader = models.ForeignKey(TeamLeader, on_delete=models.SET_NULL, null=True)
    # Employees who are invovled in certain campaign
    employees = models.ManyToManyField(Employee, related_name='campaigns')

    def __str__(self):
        return f"{self.name} - {self.start_date} to {self.end_date}"
    
    # Getting the most recent bugdet from related reports
    def get_budget(self):
        return sum(report.budget for report in self.reports.all())
    
# Creating a campaigns report model, to store budgets and reports linked to campaigns
class CampaignReport(models.Model):
    report_data = models.TextField()
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='reports')
    budget = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        # Shows the first 50 charactsers of the report data
        return f"Report for {self.campaign.name} on {self.report_data[:50]}"
    
# Creating a Task model, individual tasks assigned to employees in campaigns
class Task(models.Model):
    description = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    team_leader = models.ForeignKey(TeamLeader, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    due_date = models.DateField()

    def __str__(self):
        # Displaying first 50 character of the description
        return f"Task: {self.description[:50]}"
    
# Creating a entry model, employee work hours (for clock in/out)
class Entry(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField()
    status = models.CharField(max_length=50, default='pending')
    approved_by = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Entry for {self.employee.first_name} {self.employee.last_name}"

# Creating a payslip model, stores payroll information based on apporved entries
class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10,decimal_places=2)
    issued_date = models.DateField()
    processed_by = models.ForeignKey(PayrollTeam, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Payslip for {self.employee.first_name} {self.employee.last_name} - {self.issued_date}"