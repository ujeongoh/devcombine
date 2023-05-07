from django.contrib import admin
from .models import *
from django.forms.models import BaseInlineFormSet


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

class CategoryTagInline(admin.TabularInline):
    model = Category.tags.through
    fields = ('tag',)  # 출력하고자 하는 필드 이름
    extra = 1

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('tag')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryTagInline]
    # search_fields = ['tag']
