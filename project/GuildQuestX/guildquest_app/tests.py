from datetime import datetime, timedelta
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from GuildQuestX.guildquest_app.models import (
    Manager, Employee, TeamLeader, Campaign,
    CampaignReport, Task, PayrollTeam, Entry, Payslip
)

# Tests related to campaign setup and reporting
class CampaignTest(TestCase):
    def setUp(self):
        # Create manager user and instance
        self.manager_user = User.objects.create_user('jinwoo_sung', 'jinSun@gmail.com', 'Arise')
        self.manager = Manager.objects.create(
            user=self.manager_user,
            first_name='Jinwoo',
            last_name='Sung',
            email='jinSun@gmail.com'
        )

        # Create employee user and instance
        self.employee_user = User.objects.create_user('jungwonie_wonie', 'jywontonie@gmail.com', 'engene')
        self.employee = Employee.objects.create(
            user=self.employee_user,
            first_name='Jung',
            last_name='wonie',
            email='jywontonie@gmail.com',
            role='Developer'
        )

        # Create team leader linked to employee
        self.leader_user = User.objects.create_user('hiro_dashi', 'hiron@gmail.com', 'Baymax')
        self.team_leader = TeamLeader.objects.create(
            user=self.leader_user,
            first_name='Hiro',
            last_name='dashi',
            email='hiron@gmail.com',
            employee_ref=self.employee
        )

        # Create campaign with a time range and leader
        self.campaign = Campaign.objects.create(
            name='Spring Launch',
            description='Launch for spring campaign',
            start_date=datetime.today().date(),
            end_date=datetime.today().date() + timedelta(days=30),
            team_leader=self.team_leader
        )
        self.campaign.manager = self.manager
        self.campaign.save()
        self.campaign.employees.add(self.employee)

        # Add a campaign report with a budget
        self.report = CampaignReport.objects.create(
            report_data="Campaign went well. Budget remained in range.",
            campaign=self.campaign,
            budget=5000.00
        )

    def test_campaign_str(self):
        # Ensure the campaign string includes the name
        self.assertIn("Spring Launch", str(self.campaign))

    def test_get_campaign_budget(self):
        # Should return the total budget of the campaign (from reports)
        self.assertEqual(self.campaign.get_budget(), 5000.00)

    def test_report_str(self):
        # Ensure the report string includes part of the report text
        self.assertIn("Campaign went well", str(self.report))


# Tests related to tasks and team members
class TaskAssignmentTest(TestCase):
    def setUp(self):
        # Create employee
        self.emp_user = User.objects.create_user('jungwonie_wonie', 'jywontonie@gmail.com', 'engene')
        self.employee = Employee.objects.create(
            user=self.emp_user,
            first_name='Jung',
            last_name='wonie',
            email='jywontonie@gmail.com',
            role='Developer'
        )

        # Create team leader and link to employee
        self.lead_user = User.objects.create_user('hiro_dashi', 'hiron@gmail.com', 'Baymax')
        self.team_leader = TeamLeader.objects.create(
            user=self.lead_user,
            first_name='Hiro',
            last_name='dashi',
            email='hiron@gmail.com',
            employee_ref=self.employee
        )

        # Link the employee to the team leader
        self.employee.team_leader = self.team_leader
        self.employee.save()

        # Create a campaign and assign employee
        self.campaign = Campaign.objects.create(
            name='Summer Ops',
            description='Ops for summer',
            start_date=datetime.today().date(),
            end_date=datetime.today().date() + timedelta(days=60),
            team_leader=self.team_leader
        )
        self.campaign.employees.add(self.employee)

        # Assign a task to employee under the campaign
        self.task = Task.objects.create(
            description='Finish frontend module',
            employee=self.employee,
            campaign=self.campaign,
            team_leader=self.team_leader,
            status='in progress',
            due_date=datetime.today().date() + timedelta(days=10)
        )

    def test_task_str(self):
        # Task string should include task description
        self.assertIn('Finish frontend', str(self.task))

    def test_team_leader_gets_employee(self):
        # Team leader should be able to retrieve their team member
        team = self.team_leader.get_team_member()
        self.assertIn(self.employee, team)

# Tests related to entries and payslip generation
class PayslipTest(TestCase):
    def setUp(self):
        # Create payroll team member
        self.payroll_user = User.objects.create_user('krabs_krabby', 'KrabsMon@gmail.com', 'Money')
        self.payroll_team = PayrollTeam.objects.create(
            user=self.payroll_user,
            first_name='Krabs',
            last_name='Krabby',
            email='KrabsMon@gmail.com'
        )

        # Create employee
        self.emp_user = User.objects.create_user('jungwonie_wonie', 'jywontonie@gmail.com', 'engene')
        self.employee = Employee.objects.create(
            user=self.emp_user,
            first_name='Jung',
            last_name='wonie',
            email='jywontonie@gmail.com',
            role='Developer'
        )

        # Create manager who approves entries
        self.manager_user = User.objects.create_user('jinwoo_sung', 'jinSun@gmail.com', 'Arise')
        self.manager = Manager.objects.create(
            user=self.manager_user,
            first_name='Jinwoo',
            last_name='Sung',
            email='jinSun@gmail.com'
        )

        # Create entry for hours worked
        self.entry = Entry.objects.create(
            employee=self.employee,
            hours_worked=8.5,
            clock_in=timezone.make_aware(datetime(2024, 4, 1, 9, 0)),
            clock_out=timezone.make_aware(datetime(2024, 4, 1, 17, 30)),
            status='approved',
            approved_by=self.manager
        )

        # Generate payslip for the entry
        self.payslip = Payslip.objects.create(
            employee=self.employee,
            entry=self.entry,
            salary=400.00,
            deductions=50.00,
            bonus=20.00,
            issued_date=datetime.today().date(),
            processed_by=self.payroll_team
        )

    def test_entry_str(self):
        # Entry string should include employee's name
        self.assertIn('Jung wonie', str(self.entry))

    def test_payslip_str(self):
        # Payslip string should include employee info
        self.assertIn('Payslip for Jung wonie', str(self.payslip))
