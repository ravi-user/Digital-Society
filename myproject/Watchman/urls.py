"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from Watchman import views

urlpatterns = [
    path('sign-up',views.sign_up, name="sign-up"),
    path('w-dashboard',views.w_dashboard, name="w-dashboard"),
    path('w-profile', views.w_profile, name="w-profile"),
    path('w-all-member', views.w_all_member, name='w-all-member'),
    path('w-all-notice', views.w_all_notice, name='w-all-notice'),
    path('w-all-event', views.w_all_event, name='w-all-event'),
    path('w-add-visitor', views.w_add_visitor, name='w-add-visitor'),
    path('w-all-visitor', views.w_all_visitor, name='w-all-visitor'),


]
