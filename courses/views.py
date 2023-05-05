from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from .models import Course, Tag

from django.middleware.csrf import get_token
from django.urls import reverse
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.forms.models import model_to_dict



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


def all_courses(request):
    """
    전체 코스 조회, 필터링 기능
    """
    course_info_list = []

    all_courses = Course.objects.all()
    for course in all_courses:
        course_info = model_to_dict(course)  # 객체 import
        course_info_list.append(course_info)
    context = {
        'all_courses': course_info_list
    }
    # print(context)
    return render(request, 'courses/all_courses.html', context)

