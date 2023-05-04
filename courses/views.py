from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Course, UserProfile
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return JsonResponse({
                'message': '회원가입이 성공적으로 완료되었습니다.',
                'user_id': user.id
            })
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
            return JsonResponse({
                'message': '로그인이 성공적으로 완료되었습니다.',
                'user_id': user.id,
                'access_token': 'TODO',
            })
        else:
            return JsonResponse({'error': 'Invalid credentials.'}, status=401)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'message': '로그아웃이 성공적으로 완료되었습니다.'})


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