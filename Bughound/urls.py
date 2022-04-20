"""Bughound URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    # ex: /polls/
    path('', views.dashboard, name='index'),
    path('login/', views.login, name='login'),
    #path('login/?P<str>', views.redirect, name='redirect'),

    #path('logout/', views.logout, name='logout'),
   # path('register/', views.register, name='register'),
    #path('profile/', views.profile, name='profile'),
   # path('profile/edit/', views.edit_profile, name='edit_profile'),
    #path('profile/change_password/', views.change_password, name='change_password'),
    #path('profile/change_password/done/', views.change_password_done, name='change_password_done'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('report/', views.report, name='report'),
    path('reports/<int:id>/', views.reportUpdate, name='report_detail'),
    path('reports/', views.reports, name='reports'),
    path('ajax/load-areas/', views.load_areas, name='ajax_load_areas'),  # ajax
    path('maintenance/', views.maintenance, name='maintenance'),
    path('maintenance/<str:id>/', views.maintenance_detail, name='maintenance_detail'),
    path('maintenance/<str:name>/<int:object_id>/', views.edit, name='maintenance_edit'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('settings/', views.settings, name='settings'),
]
