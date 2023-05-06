from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.total_course, name='total_course'),
    path('admin/upload-csv/', views.upload_csv, name='upload_csv'),
]
