from django.contrib import admin
from django.urls import path
from .views import *

app_name='common'
urlpatterns = [
    path('home/', home),
    path('monitor_all/', monitor_all),
    path('study_well/', study_well),
    path('study_poor/', study_poor),
    path('admin/', admin),
    path('first/', first),
    path('login/', login),
    path('register/', register),
    path('reset/', reset),
    path('inquiry/', inquiry),
    path('base/', base),
    path('supervision/', supervision)
]