from django.contrib import admin
from .models import *
from .forms import CSVUploadForm
from django.shortcuts import render
from django.urls import path


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'instructor', 'site', 'price')
    change_list_template = 'admin/courses/course/course_change_list.html'

admin.site.register(Tag)
admin.site.register(UserProfile)