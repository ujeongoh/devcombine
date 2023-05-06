from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Series, SeriesTag


class SeriesTagInline(admin.TabularInline):
    model = SeriesTag  # Series.tags.through
    extra = 0


class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_main', 'display_series_tags')
    inlines = [SeriesTagInline]
    list_filter = ('is_main', 'create_at')    # 필터를 통해, Series를 관리한다.
    readonly_fields = ['create_at']
    search_fields = ["tags__name"]

    def display_series_tags(self, obj) -> str:
        """
        Series Admin 창에서, 지정한 Tags를 확인할 수 있게 하는 함수
        """
        series_tags = SeriesTag.objects.filter(series_id=obj)
        tag_names = [str(series_tag.tag_id) for series_tag in series_tags]
        return ', '.join(tag_names)

    display_series_tags.short_description = "Series Tags"


admin.site.register(Series, SeriesAdmin)
