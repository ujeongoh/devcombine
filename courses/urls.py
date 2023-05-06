from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.total_course, name='total_course'),
    path('admin/upload-csv/', views.upload_csv, name='upload_csv'),
    path('<int:course_id>/likes/', views.like_course, name='like_course'),
    path('<int:course_id>/dislikes/', views.dislike_course, name='dislike_course'),
    path('<int:course_id>/likes/check/', views.check_course_like, name='check_course_like'),
    path('<int:course_id>/likes/count/', views.course_like_count, name='course_like_count')
]
