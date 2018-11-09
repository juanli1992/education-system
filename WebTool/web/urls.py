from django.contrib import admin
from django.urls import path
from .views import homepage

app_name='common'
urlpatterns = [
    path('', homepage),
]