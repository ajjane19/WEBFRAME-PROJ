from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "polls"

# Define the URL patterns for each role-specific dashboard
urlpatterns = [
    # General paths
    path("", views.index, name="index"),
    path("login/", views.custom_login, name="login"),
    path("logout/", LogoutView.as_view(next_page="polls:index"), name="logout"),

    # Role-based dashboard paths

    # For guests and general dashboard
    path("dashboard/", views.dashboard, name="dashboard"),  
    # Manager dashboard
    path("manager/dashboard/", views.manager_dashboard, name="manager_dashboard"),  
    # Employee dashboard
    path("employee/dashboard/", views.employee_dashboard, name="employee_dashboard"),  
    # Payroll team dashboard
    path("payroll/dashboard/", views.payroll_dashboard, name="payroll_dashboard"),  
    # Team leader dashboard
    path("teamleader/dashboard/", views.teamleader_dashboard, name="teamleader_dashboard"),  
    # Guest dashboard
    path("guest/dashboard/", views.guest_dashboard, name="guest_dashboard"),  

    # For Employees to submit work entries
    path("submit-entry/", views.submit_entry, name="submit_entry"),

    # For Team leader to assign tasks and monitor campaigns
    path('assign-task/', views.assign_task, name='assign_task'),
    path('update_campaign_report/', views.update_campaign_report, name='update_campaign_report'),

    # For Manager to approve and reject entries
    path('appove-entry/<int:id>/', views.approve_entry, name='approve_entry'),
    path('reject-entry/<int:id>/', views.reject_entry, name='reject_entry'),

    # For Payroll Team member to process payroll and generate payslip
    path('process-payslip/', views.process_payslip, name='process_payslip'),
]
