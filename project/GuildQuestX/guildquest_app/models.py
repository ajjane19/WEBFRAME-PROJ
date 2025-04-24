from django.db import models
from django.contrib.auth.models import User

# Creating a manager model - which will be used to approve entries and generate campaign reports
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Creating a payroll team member model - used to represent users who process payslips after approval
class PayrollTeam(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Creating a Employee model - Regular users who clock in/out and view their payslip
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    team_leader = models.ForeignKey('TeamLeader', on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Creating a Team Leader model - these users assign tasks to employees and monitor progress in campaign
class TeamLeader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    employee_ref = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='as_team_leader')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # Getting all employees under certain team leader
    def get_team_member(self):
        return Employee.objects.filter(team_leader=self)

    # Get all campaigns this team leader is managing
    def get_campaigns(self):
        return Campaign.objects.filter(team_leader=self)

# Creating a campaigns model, projects that employees are assigned to
class Campaign(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    team_leader = models.ForeignKey(TeamLeader, on_delete=models.SET_NULL, null=True)
    employees = models.ManyToManyField(Employee, related_name="campaigns")

    def __str__(self):
        return f"{self.name} - {self.start_date} to {self.end_date}"

    # Getting the most recent budget from related reports
    def get_budget(self):
        return sum(report.budget for report in self.reports.all())

# Creating a campaigns report model - to store budgets and reports linked to campaigns
class CampaignReport(models.Model):
    report_data = models.TextField()
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='reports')
    budget = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Report for {self.campaign.name} on {self.report_data[:50]}"

# Creating a Task model - individual tasks assigned to employees in campaigns
class Task(models.Model):
    # Define the foreign keys to Employee, TeamLeader, and Campaign
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='tasks')
    team_leader = models.ForeignKey('TeamLeader', on_delete=models.CASCADE, related_name='tasks')
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE, related_name='tasks')
    
    # Define other fields
    description = models.TextField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('in_progress', 'In Progress')], default='pending')
    due_date = models.DateField()

    def __str__(self):
        return f"Task: {self.description} assigned to {self.employee.first_name} {self.employee.last_name}"

# Creating an entry model - employee work hours (for clock in/out)
class Entry(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField()
    status = models.CharField(max_length=20)
    approved_by = models.ForeignKey(Manager, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Entry for {self.employee.first_name} {self.employee.last_name}"

# Creating a payslip model - stores payroll information based on approved entries
class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payslips")
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateField(auto_now_add=True)
    processed_by = models.ForeignKey(PayrollTeam, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Payslip for {self.employee.first_name} {self.employee.last_name} - {self.issued_date}"
