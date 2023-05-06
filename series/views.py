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
    def series_course_info_list(matching_courses) -> list :
        # Series에 해당하는 전체 코스 함수
        total_series_course = []
        for course in matching_courses :
            course_info = model_to_dict(course)
            total_series_course.append(course_info)
        return total_series_course
        

    def get(self, request, series_id) :
        # API : /series/{series_id}/
        series = Series.objects.get(id=series_id)
        series_tags = series.tags.all()        # series에 들어있는 태그를 모두 가져온다.
        
        # 일치하는 Course 찾기
        matching_courses = Course.objects.filter(tags__in = series_tags).distinct()
        
        context = {
            'series' : series,
            'matching_courses' : matching_courses,
            'series_tags' :series_tags,
            'series_course_info_list' : self.series_course_info_list(matching_courses)   
        } 
        
        # context 에 Pagenator 설정 필요 
        
        return render(request, 'seires/series_course.html', context)    

def main_series(request):
    """
    메인에 노출 시키는 시리즈의 목록만 가져오는 함수
    - Admin에서 Sries를 지정할 때 is_main = True 로 노출 시킨 값만 필터링 한다.
    """
    main_series = Series.objects.filter(is_main=True).order_by(Random())[:3]        # main화면에 3개만 Random

    # for series in main_series :
    #     # 메인에 View 될 series
    
    

    context = {
        'main_series': main_series
    }

    return render(request, 'series/index.html', context)


def series_list(request):
    """
    전체 시리즈의 목록을 가져오는 함수
    """
    # test 용
    series_list = Series.objects.all()

    return render(request, 'series/index.html')


def series_course(request, series_id):
    """
    시리즈에 해당하는 코스 조회
    TODO
    1. GET /series/1/ 입력 받으면, Pagenation 지정이 가능한 페이지가 노출되어야 함
    2. 이 함수는 seires_course에 대한 정보를 모두 가지고 있으므로, main_series가 호출되면, 이 함수 내의 context를 return 해주어야 한다.
    """
    series = Series.objects.get(pk=series_id)
    tags = series.tags.all()            # series에 들어있는 들어있는 태그를 모두 가져온다.
    # 태그값으로 필터링 된 코스를 가져온다.
    courses = Course.objects.filter(tags__in=tags).annotate(
        tag_count=Count('tags')).order_by('-tag_count')

    series_course_info_list = []

    for course in courses:
        course_info = model_to_dict(course)
        series_course_info_list.append(course_info)

    context = {
        'series': series,
        'courses': courses,
        'tags': tags,
        'series_course': series_course_info_list
    }
    # print(context)
    return render(request, 'series/series_course.html', context)
