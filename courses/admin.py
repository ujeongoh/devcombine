from django.contrib import admin
from .models import *


admin.site.register(Tag)
admin.site.register(CourseTag)


class CourseTagInline(admin.TabularInline):
    model = CourseTag
    extra = 0


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'site', 'price')
    inlines = [CourseTagInline]
    list_filter = ('tags__name', 'update_at')
    readonly_fields = ['update_at']
    search_fields = ["tags__name"]
    change_list_template = 'admin/courses/course_change_list.html'


admin.site.register(Course, CourseAdmin)
