from django.contrib import admin
from django.urls import path
from .views import *

app_name='common'
urlpatterns = [
    path('home/', homepage),
    path('monitor_all/', monitor_all),
    path('study_well/', study_well),
    path('study_poor/', study_poor),
]