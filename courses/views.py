from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, 'courses/index.html')


def series(request):
    """
    시리즈명 조회
    """
    return "test"

def series_detail(request, series_id):
    """
    시리즈에 해당하는 코스 조회 (SeriesCourse model)
    """

    return render(request, 'courses/detail.html')