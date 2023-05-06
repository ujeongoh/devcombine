from django.contrib.auth.models import User
from .forms import CSVUploadForm
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Course, Tag
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
import csv
from io import TextIOWrapper
from datetime import datetime
from decimal import Decimal, InvalidOperation


def total_course(request):
    """
    전체 코스 조회, 필터링 기능
    """
    selected_tag_ids = request.GET.getlist('tags')
    selected_tags = [int(tag_id) for tag_id in selected_tag_ids]
    if selected_tags:
        total_course = Course.objects.filter(tags__id__in=selected_tags).distinct()
    else:
        total_course = Course.objects.all()

    all_tags = Tag.objects.all()[:10] #todo::몇개를 하는게 좋을까요?

    context = {
        'total_course': total_course,
        'all_tags': all_tags,
        'selected_tags': selected_tags,
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


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_course(request, course_id):
    course = Course.objects.get(id=course_id)
    user_id = request.data.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        course.likes.add(user)
        course.dislikes.remove(user)
        return JsonResponse({}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def dislike_course(request, course_id):
    course = Course.objects.get(id=course_id)
    user_id = request.data.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        course.dislikes.add(user)
        course.likes.remove(user)
        return JsonResponse({}, status=202)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def check_course_like(request, course_id):
    course = Course.objects.get(id=course_id)
    user_id = request.data.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        if user in course.likes.all():
            check = 1
        else:
            check = 0
        return JsonResponse({'check': check})
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


# TODO 이유는 모르겠지만 빈 wishlist반환됨.


# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def user_wishlist(request):
#     user_id = request.data.get('user_id')
#     if user_id:
#         user = User.objects.get(id=user_id)
#         interests = user.userprofile.interests.all()
#         wishlist = []
#         for interest in interests:
#             wishlist.append({
#                 'id': interest.id,
#                 'courses': {
#                     'course_id': interest.id,
#                     'course_name': interest.title,
#                 }
#             })
#         return JsonResponse({'wishlist': wishlist}, status=200)
#     else:
#         return JsonResponse({'error': 'Invalid request.'}, status=400)


@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def course_like_count(request, course_id):
    course = Course.objects.get(id=course_id)
    count = course.likes.count()
    return JsonResponse({'like_count': count})