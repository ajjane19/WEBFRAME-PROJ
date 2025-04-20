from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.index, name="index"), 
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/guest/", views.dashboard, name="guest"),
    path("login/", LoginView.as_view(template_name="polls/login.html"), name='login'), #login page
    path("logout/", LogoutView.as_view(next_page="index"), name='logout',)
]