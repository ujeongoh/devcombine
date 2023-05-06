from django.forms import model_to_dict
from django.shortcuts import render
from django.db.models import Count
from django.views.generic import ListView
from django.db.models.functions import Random


from courses.models import Course
from series.models import Series

# class SeriesListView(ListView):
#     """
#     SeriesListView
#     - 전체 시리즈
#     """
#     model = Series
#     context_object_name = 'series_list'
#     template_name = 'series/index.html'

#     # /series/list/ 라고 치면 Total series가 나와야 함


class SereisCourseListView(ListView):
    """
    SeriesCourseListView : 태그값으로 필터링 된 View
    """

    def get(self, request, series_id):
        # API : /series/{series_id}/
        series = Series.objects.get(id=series_id)
        series_tags = series.tags.all()        # series에 들어있는 태그를 모두 가져온다.

        # 일치하는 Course 찾기
        matching_courses = Course.objects.filter(
            tags__in=series_tags).distinct()

        context = {
            'series': series,
            'matching_courses': matching_courses,
        }
        
        # TODO :: context 에 Pagenator 설정 필요

        return render(request, 'series/series_course.html', context)


def main_series(request):
    """
    메인에 노출 시키는 시리즈의 목록만 가져오는 함수
    - Admin에서 Sries를 지정할 때 is_main = True 로 노출 시킨 값만 필터링 한다.
    """
    main_series = Series.objects.filter(is_main=True).order_by(Random())[
        :3]        # main화면에 3개만 Random

    return render(request, 'series/index.html', {'main_series' : main_series})