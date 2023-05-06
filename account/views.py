from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import UserProfile
from .serializers import MyTokenObtainPairSerializer
from .forms import CustomUserCreationForm

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
            return HttpResponseRedirect(reverse('series:main_series'))
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
            return HttpResponseRedirect(reverse('series:main_series'))
        else:
            return JsonResponse({'error': 'Invalid credentials.'}, status=401)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('series:main_series'))


