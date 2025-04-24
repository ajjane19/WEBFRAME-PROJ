from django.contrib import admin
from .models import Manager, PayrollTeam, Employee, TeamLeader, Campaign, Task, Entry, Payslip, CampaignReport

# Registering Model to appear in the admin interface
admin.site.register(Manager)
admin.site.register(PayrollTeam)
admin.site.register(Employee)
admin.site.register(TeamLeader)
admin.site.register(Campaign)
admin.site.register(Task)
admin.site.register(Entry)
admin.site.register(Payslip)
admin.site.register(CampaignReport)
