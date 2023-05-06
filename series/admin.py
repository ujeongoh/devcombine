from django.contrib import admin
from .models import Series

class SeriesTagInline(admin.TabularInline):
    model = Series.tags.through


class SeriesAdmin(admin.ModelAdmin):
    inlines = [SeriesTagInline]

admin.site.register(Series, SeriesAdmin)