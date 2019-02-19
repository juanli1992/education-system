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
    path('supervision/', supervision),
    path('result/', result),
    path('query/', query),
    path('query1/', query1),
    path('queryY/', queryY),
    path('data_import_export/', data_import_export),
    path('intervene/', intervene),
    path('CheckData/', CheckData),
    path('View/', View),
    path('download/', download),
    path("query_intervene", query_intervene),
    path('query_majors', query_majors)
]