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

def index(request):
    return render(request, 'base_index.html')


@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return HttpResponseRedirect(reverse('account:index'))
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
            return HttpResponseRedirect(reverse('account:index'))
        else:
            return JsonResponse({'error': 'Invalid credentials.'}, status=401)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('account:index'))


