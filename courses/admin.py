from django.contrib import admin
from .models import *


admin.site.register(Tag)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'instructor', 'site', 'price')
    change_list_template = 'admin/courses/course/course_change_list.html'