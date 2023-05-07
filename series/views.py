from django.shortcuts import render
from django.db.models import Count
from django.views.generic import ListView
from django.db.models.functions import Random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from courses.models import Course
from series.models import Series


class SeriesListView(ListView):
    """
    SeriesListView
    - 전체 시리즈
    """
    model = Series
    template_name = 'series/index.html'
    context_object_name = 'main_series'

    def get_queryset(self):
        """
        메인에 노출 시키는 시리즈의 목록만 가져오는 함수
        - Admin에서 Sries를 지정할 때 is_main = True 로 노출 시킨 값만 필터링 한다.
        """
        main_series = Series.objects.filter(is_main=True).order_by(Random())[
            :3]        # main화면에 3개만 Random

        return main_series


class SereisCourseListView(ListView):
    """
    SeriesCourseListView : 태그값으로 필터링 된 View
    """

    def get(self, request, series_id):
        # API : /series/{series_id}/
        series = Series.objects.get(id=series_id)
        series_tags = series.tags.all()        # series에 들어있는 태그를 모두 가져온다.

        # Series의 Course 찾기
        series_courses = Course.objects.filter(
            tags__in=series_tags).distinct()

        # Series의 Course에서, paging 처리 => series_courses
        page = request.GET.get('page', 1)
        series_courses_pagenator = Paginator(series_courses, 12)
        page_obj = series_courses_pagenator.page(page)

        try:
            series_courses = series_courses_pagenator.page(page)
        except PageNotAnInteger:
            series_courses = series_courses_pagenator.page(1)
        except EmptyPage:
            series_courses = series_courses.page(
                series_courses_pagenator.num_pages)

        context = {
            'series': series,
            'series_tags': series_tags,
            'series_courses': series_courses,
        }

        return render(request, 'series/series_course.html', context)


# class SeriesListView(ListView):
#     """
#     SeriesListView
#     - 전체 시리즈
#     """
#     model = Series
#     template_name = 'series/index.html'
#     context_object_name = 'main_seiries'
#     def get(self, request):
#         """
#         메인에 노출 시키는 시리즈의 목록만 가져오는 함수
#         - Admin에서 Sries를 지정할 때 is_main = True 로 노출 시킨 값만 필터링 한다.
#         """
#         main_series = Series.objects.filter(is_main=True).order_by(Random())[
#             :3]        # main화면에 3개만 Random

#         return render(request, 'series/index.html', {'main_series': main_series})

#     # /series/list/ 라고 치면 Total series가 나와야 함
