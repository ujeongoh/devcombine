from django.contrib import admin
from .models import *


admin.site.register(Tag)
admin.site.register(CourseTag)


class CourseTagInline(admin.TabularInline):
    model = Course.tags.through


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'instructor', 'site', 'price')
    inlines = [CourseTagInline]
    change_list_template = 'admin/courses/course_change_list.html'


admin.site.register(Course, CourseAdmin)
