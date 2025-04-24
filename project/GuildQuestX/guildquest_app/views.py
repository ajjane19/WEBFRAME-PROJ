from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Manager, Employee, PayrollTeam, TeamLeader, Entry, Campaign, Payslip, CampaignReport, Task
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone

# Home page (for guests or general page)
def index(request):
    return render(request, 'guildquest_app/index.html')

# Dashboard view for logged-in users and guests
def dashboard(request):
    user = request.user

    if user.is_authenticated:
        # User is logged in, check role and render the appropriate dashboard
        if Manager.objects.filter(user=user).exists():
            return render(request, 'polls/dashboards/manager.html', {'manager': user.manager})

        elif Employee.objects.filter(user=user).exists():
            return render(request, 'polls/dashboards/employee.html', {'employee': user.employee})

        elif PayrollTeam.objects.filter(user=user).exists():
            return render(request, 'polls/dashboards/payrollteam.html', {'payroll': user.payrollteam})

        elif TeamLeader.objects.filter(user=user).exists():
            return render(request, 'polls/dashboards/teamleader.html', {'teamleader': user.teamleader})

        else:
            return render(request, 'polls/dashboards/guest.html')
    else:
        # If user is not authenticated, render the guest dashboard
        return render(request, 'polls/dashboards/guest.html')

# Custom login view
def custom_login(request):
    if request.user.is_authenticated:
        # Redirect to dashboard if already authenticated
        return redirect('polls:dashboard')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in

            # Redirect to the correct dashboard (based on their role)
            if Manager.objects.filter(user=user).exists():
                return redirect('polls:manager_dashboard') 
            elif Employee.objects.filter(user=user).exists():
                return redirect('polls:employee_dashboard') 
            elif PayrollTeam.objects.filter(user=user).exists():
                return redirect('polls:payroll_dashboard') 
            elif TeamLeader.objects.filter(user=user).exists():
                return redirect('polls:teamleader_dashboard') 
            else:
                return redirect('polls:guest_dashboard') 

    else:
        form = AuthenticationForm()

    return render(request, 'polls/registration/login.html', {'form': form})

# Define specific role dashboards
# Manager dashboard
@login_required
def manager_dashboard(request):
    user = request.user

    if Manager.objects.filter(user=user).exists():
        manager = Manager.objects.get(user=user)
        pending_entries = Entry.objects.filter(status="pending")

        selected_campaign = None
        report_entries = []
        payslips = []
        campaign_report = None

        if request.method == "POST":
            # Create Campaign
            if 'create_campaign' in request.POST:
                name = request.POST.get('name')
                description = request.POST.get('description')
                start_date_str = request.POST.get('start_date')
                end_date_str = request.POST.get('end_date')
                team_leader_id = request.POST.get('team_leader')
                employee_ids = request.POST.getlist('employees')

                start_date = parse_date(start_date_str)
                end_date = parse_date(end_date_str)

                try:
                    team_leader = TeamLeader.objects.get(id=team_leader_id)
                    campaign = Campaign.objects.create(
                        name=name,
                        description=description,
                        start_date=start_date,
                        end_date=end_date,
                        manager=manager,
                        team_leader=team_leader
                    )
                    for eid in employee_ids:
                        try:
                            employee = Employee.objects.get(id=eid)
                            campaign.employees.add(employee)
                        except Employee.DoesNotExist:
                            messages.warning(request, f"Employee with ID {eid} not found.")
                    messages.success(request, "Campaign created successfully.")
                    return redirect('polls:manager_dashboard')
                except TeamLeader.DoesNotExist:
                    messages.error(request, "Selected Team Leader does not exist.")

            # Generate Report
            elif 'generate_report' in request.POST:
                campaign_id = request.POST.get('campaign_id')
                try:
                    selected_campaign = Campaign.objects.get(id=campaign_id, manager=manager)
                    report_entries = Entry.objects.filter(campaign=selected_campaign, status="approved")
                    payslips = Payslip.objects.filter(entry__in=report_entries)

                    # Fetch or create CampaignReport
                    campaign_report, created = CampaignReport.objects.get_or_create(
                        campaign=selected_campaign,
                        defaults={
                            'report_data': 'Auto-generated summary for reporting.',
                            'budget': 0.00
                        }
                    )

                except Campaign.DoesNotExist:
                    messages.error(request, "Campaign not found or does not belong to you.")

        # Template data
        team_leaders = TeamLeader.objects.all()
        employees = Employee.objects.all()
        campaigns = Campaign.objects.filter(manager=manager)

        context = {
            'manager': manager,
            'campaigns': campaigns,
            'team_leaders': team_leaders,
            'employees': employees,
            'pending_entries': pending_entries,
            'payslips': payslips,
            'selected_campaign': selected_campaign,
            'report_entries': report_entries,
            'campaign_report': campaign_report,
        }

        return render(request, 'polls/dashboards/manager.html', context)

    return redirect('polls:index')

# Employee dashboard
def employee_dashboard(request):
    user = request.user
    if Employee.objects.filter(user=user).exists():
        return render(request, 'polls/dashboards/employee.html', {'employee': user.employee})
    # If the user is not an employee, redirect to the index page
    return redirect('polls:index')  

# Payroll dashboard
def payroll_dashboard(request):
    
    try:
        payroll_user = PayrollTeam.objects.get(user=request.user)
    except PayrollTeam.DoesNotExist:
        messages.error(request, "Unauthorized access.")
        return redirect('polls:index')

    # Approved entries that do NOT yet have a payslip
    approved_entries = Entry.objects.filter(
        status='approved'
    ).exclude(
         # Exclude entries that already have a payslip
        payslip__isnull=False 
    )

    return render(request, 'polls/dashboards/payrollteam.html', {
        'approved_entries': approved_entries
    })

@login_required
def teamleader_dashboard(request):
    teamleader = TeamLeader.objects.get(user=request.user)

    # Assign all employees to this team leader if they don’t have one
    unassigned_employees = Employee.objects.filter(team_leader__isnull=True)
    for emp in unassigned_employees:
        emp.team_leader = teamleader
        emp.save()

    # Now get the employees assigned to this team leader
    employees = teamleader.get_team_member()

    # Fetch ongoing campaigns
    campaigns = teamleader.get_campaigns()

    return render(request, 'polls/dashboards/teamleader.html', {
        'teamleader': teamleader,
        'employees': employees,
        'campaigns': campaigns,
    })

def guest_dashboard(request): 
    # Fallback dashboard for users with no role
    return render(request, 'polls/dashboards/guest.html') 

@login_required
def submit_entry(request):
    if request.method == "POST":
        # Get the logged-in employee
        employee = request.user.employee

        # Get the form data (clock_in and clock_out as strings)
        hours_worked = request.POST.get('hours_worked')
        clock_in_str = request.POST.get('clock_in')
        clock_out_str = request.POST.get('clock_out')

        # Directly use the clock_in and clock_out values (assumed to be in correct format)
        if clock_in_str and clock_out_str:
            Entry.objects.create(
                employee=employee,
                hours_worked=hours_worked,
                # Django handles the format
                clock_in=clock_in_str, 
                clock_out=clock_out_str,  
                 # Set the status to "pending" by default
                status="pending" 
            )

        else:
            # If any of the times are missing, show an error
            return redirect('polls:error')

    # After submitting the entry, redirect to the employee's dashboard
    return redirect('polls:employee_dashboard')

@login_required
def assign_task(request):
    teamleader = TeamLeader.objects.get(user=request.user)
    employees = teamleader.get_team_member()
    campaigns = teamleader.get_campaigns()

    if request.method == 'POST':
        employee_id = request.POST.get('employee') 
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        campaign_id = request.POST.get('campaign')

        if employee_id and description and due_date and campaign_id:
            employee = Employee.objects.get(id=employee_id)
            campaign = Campaign.objects.get(id=campaign_id)

            Task.objects.create(
                employee=employee,
                team_leader=teamleader,
                campaign=campaign,
                description=description,
                due_date=due_date
            )
            return redirect('polls:dashboard')

    return render(request, 'polls/dashboards/teamleader.html', {
        'teamleader': teamleader,
        'employees': employees,
        'campaigns': campaigns
    })

# For manager to approve entries
def approve_entry(request, id):
    try:
        entry = Entry.objects.get(id=id)

        if entry.status != 'approved':
            entry.status = 'approved'
            # This is where the manager is assigned
            entry.approved_by = request.user  
            entry.save()

        return redirect('polls:manager_dashboard')

    except Entry.DoesNotExist:
        return redirect('polls:manager_dashboard')

# For manager to reject entries
def reject_entry(request, id):
    try:
        entry = Entry.objects.get(id=id)
        entry.status = 'rejected' 
        entry.save()

        # Redirect back to the manager dashboard or another page
        return redirect('polls:manager_dashboard') 
    except Entry.DoesNotExist:
        return redirect('polls:manager_dashboard')  

@require_POST
def update_campaign_report(request):
    campaign_id = request.POST.get("campaign_id")
    notes = request.POST.get("report_data")
    budget = request.POST.get("budget")  
    try:
        campaign = Campaign.objects.get(id=campaign_id)

        report, created = CampaignReport.objects.get_or_create(
            campaign=campaign,
            defaults={
                "report_data": notes,
                "budget": budget 
            }
        )

        if not created:
            report.report_data = notes
            report.budget = budget  
            report.save()

        messages.success(request, "Campaign report updated successfully.")
        return redirect('polls:teamleader_dashboard')

    except Campaign.DoesNotExist:
        messages.error(request, "Campaign not found.")
        return redirect('polls:teamleader_dashboard')

@login_required
@require_POST
def process_payslip(request):
    if not hasattr(request.user, 'payrollteam'):
        return redirect('polls:index')

    entry_id = request.POST.get('entry_id')
    salary = request.POST.get('salary')
    deductions = request.POST.get('deductions')
    bonus = request.POST.get('bonus')

    try:
        entry = Entry.objects.get(id=entry_id)

        # Skip if a payslip already exists for this entry
        if Payslip.objects.filter(entry=entry).exists():
            messages.warning(request, "Payslip already exists for this entry.")
            return redirect('polls:payroll_dashboard')

        Payslip.objects.create(
            employee=entry.employee,
            entry=entry,
            salary=salary,
            deductions=deductions,
            bonus=bonus,
            issued_date=timezone.now().date(),
            processed_by=request.user.payrollteam
        )

        messages.success(request, "Payslip processed successfully.")
        return redirect('polls:payroll_dashboard')

    except Entry.DoesNotExist:
        messages.error(request, "Entry not found.")
        return redirect('polls:payroll_dashboard')

@login_required
def generate_payslip(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    if entry.status == 'approved':
        # Calculate salary, deductions, and bonus
        # Replace with actual calculation
        salary = entry.hours_worked * hourly_rate  
        # Implement this function
        deductions = calculate_deductions(entry)  
        # Implement this function
        bonus = calculate_bonus(entry)  

        # Create payslip
        payslip = Payslip.objects.create(
            employee=entry.employee,
            entry=entry,
            salary=salary,
            deductions=deductions,
            bonus=bonus,
            processed_by=request.user,
        )

        # Update entry status
        entry.status = 'processed'
        entry.save()

        return redirect('polls:view_payslip', payslip_id=payslip.id)
    else:
        return render(request, 'error.html', {'message': 'Entry not approved'})

@login_required
def view_payslip(request, payslip_id):
    payslip = Payslip.objects.get(id=payslip_id)
    if payslip.employee == request.user.employee:
        return render(request, 'view_payslip.html', {'payslip': payslip})
    else:
        return render(request, 'error.html', {'message': 'Access denied'})
