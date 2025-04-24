"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from GuildQuestX.guildquest_app import views

urlpatterns = [
    # Url for accessing the admin panel
    path("admin/", admin.site.urls),
    # Including urls from the guildquest_app and giving it a namespace for easy url ref
    path("guildquest/", include(("GuildQuestX.guildquest_app.urls", "polls"), namespace="polls")),
    # Url for the homepage, trigger the 'index' view from guildquest_app
    path("", views.index),
]

