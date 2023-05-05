from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import UserProfile
from courses.models import Course, Tag
from .serializers import MyTokenObtainPairSerializer
from .forms import CustomUserCreationForm

import csv
from io import TextIOWrapper
from datetime import datetime
from decimal import Decimal, InvalidOperation

# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrf_token': token})


@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return HttpResponseRedirect(reverse('courses:index'))
        else:

            return JsonResponse({'error': 'Invalid request.'}, status=400)
    else:
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return HttpResponseRedirect(reverse('courses:index'))
        else:
            return JsonResponse({'error': 'Invalid credentials.'}, status=401)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('courses:index'))


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


# @csrf_exempt
# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# def course_like_count(request, course_id):
#     course = Course.objects.get(id=course_id)
#     count = course.likes.count()
#     return JsonResponse({'like_count': count})




def upload_csv_view(request):
    if request.method == 'POST' and request.FILES:
        csv_file = request.FILES['csv_file']
        # CSV 파일 처리 코드 작성
        reader = csv.reader(csv_file)
        for row in reader:
            title = row[1]
            # 각 행에 대한 처리 코드 작성
        return render(request, 'admin/upload_csv_success.html')
    else:
        return render(request, 'admin/upload_csv_form.html')
