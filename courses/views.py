import csv
from io import TextIOWrapper
from django.contrib.auth.models import User

from django.shortcuts import render, redirect

from courses.forms import CSVUploadForm
from .models import Course, Tag

from django.middleware.csrf import get_token
from django.urls import reverse
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.forms.models import model_to_dict


def total_course(request):
    """
    전체 코스 조회, 필터링 기능
    """
    # TODO :: Tag 기준 필터링 기능 개발 필요

    course_info_list = []

    total_course = Course.objects.all()[:10]  # 임시로 10개만

    for course in total_course:
        course_info = model_to_dict(course)  # 객체 import
        course_info_list.append(course_info)

    context = {
        'total_course': course_info_list
    }

    return render(request, 'courses/index.html', context)


def upload_csv(request):
    """
    Course 리스트 업데이트 함수
    API : POST courses/admin/upload-csv/
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # CSV 파일을 읽기 모드로 열기
            csv_file = TextIOWrapper(
                request.FILES['csv_file'].file, encoding='utf-8')
            # CSV 파일 파싱하여 Course 모델에 저장
            reader = csv.reader(csv_file)
            next(reader)  # CSV 헤더를 건너뛰기
            now = datetime.now().date()
            for row in reader:
                site = row[0]
                title = row[1]
                instructor = row[2]
                description = row[3]
                url = row[4]
                try:
                    price = Decimal(row[5])
                except InvalidOperation:
                    price = Decimal('0.00')
                tags = row[6]
                rating = row[7]
                try:
                    rating = round(Decimal(row[7]), 3)
                except InvalidOperation:
                    rating = Decimal('0.000')
                thumbnail_url = row[8]
                is_package = bool(row[9])
                is_free = bool(row[10])
                enrollment_count_str = row[11]
                if enrollment_count_str == "" or enrollment_count_str == "0.0":
                    enrollment_count = 0
                else:
                    enrollment_count = int(float(enrollment_count_str))

                upload_date = now

                # Course 모델에 데이터 저장
                course = Course.objects.create(
                    title=title,
                    instructor=instructor,
                    description=description,
                    site=site,
                    url=url,
                    price=price,
                    rating=rating,
                    thumbnail_url=thumbnail_url,
                    is_package=is_package,
                    is_free=is_free,
                    enrollment_count=enrollment_count,
                    # upload_date=upload_date,
                )
                for tag_name in tags.split(','):
                    tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                    course.tags.add(tag)

            return render(request, 'admin/upload_success.html')
    else:
        form = CSVUploadForm()
    return render(request, 'admin/upload.html', {'form': form})
