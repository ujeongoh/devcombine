from django.contrib import admin
from .models import *
from .forms import CSVUploadForm


class CourseTagInline(admin.TabularInline):
    model = Course.tags.through


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'instructor', 'site', 'price')
    inlines = [CourseTagInline]
    change_list_template = 'admin/courses/course/course_change_list.html'


class SeriesTagInline(admin.TabularInline):
    model = Series.tags.through


class SeriesAdmin(admin.ModelAdmin):
    inlines = [SeriesTagInline]

admin.site.register(CourseTag)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Tag)
admin.site.register(UserProfile)
