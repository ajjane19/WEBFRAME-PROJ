import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.contrib.auth.models import User
from GuildQuestX.guildquest_app.models import Manager, Employee, TeamLeader, PayrollTeam

# Creating a function to create users and assign them to different models
def create_users():
    # Creating manager user
    manager_user = User.objects.create_user('jinwoo_sung', 'jinSun@gmail.com', 'Arise')
    manager_user.first_name = 'Jinwoo'
    manager_user.last_name = 'Sung'
    manager_user.save()

    # Create the manager object associated with this user
    manager = Manager.objects.create(
        user=manager_user,  # Associate user with Manager
        first_name=manager_user.first_name,
        last_name=manager_user.last_name,
        email=manager_user.email
    )
    print(f"Campaign Manager created: {manager}")

    # Creating employee user
    employee_user = User.objects.create_user('jungwonie_wonie', 'jywontonie@gmail.com', 'engene')
    employee_user.first_name = 'Jung'
    employee_user.last_name = 'wonie'
    employee_user.save()

    # Create the employee object associated with this user
    employee = Employee.objects.create(
        user=employee_user,  # Associate user with Employee
        first_name=employee_user.first_name,
        last_name=employee_user.last_name,
        email=employee_user.email
    )
    print(f"Campaign Employee created: {employee}")

    # Creating team leader user
    leader_user = User.objects.create_user('hiro_dashi', 'hiron@gmail.com', 'Baymax')
    leader_user.first_name = 'Hiro'
    leader_user.last_name = 'dashi'
    leader_user.save()

    # Create the team leader object
    team_leader = TeamLeader.objects.create(
        user=leader_user,  # Associate user with TeamLeader
        first_name=leader_user.first_name,
        last_name=leader_user.last_name,
        email=leader_user.email,
        employee_ref=employee  # Link to employee
    )
    print(f"Campaign Team Leader created: {team_leader} and linked to {employee}")

    # Creating payroll team member
    payroll_user = User.objects.create_user('krabs_krabby', 'KrabsMon@gmail.com', 'Money')
    payroll_user.first_name = 'Krabs'
    payroll_user.last_name = 'Krabby'
    payroll_user.save()

    # Create the payroll team object
    payroll_team = PayrollTeam.objects.create(
        user=payroll_user,  # Associate user with PayrollTeam
        first_name=payroll_user.first_name,
        last_name=payroll_user.last_name,
        email=payroll_user.email
    )
    print(f"Campaign Payroll Team Member created: {payroll_team}")

create_users()
