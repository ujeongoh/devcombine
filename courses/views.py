from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'courses/index.html')


def series_detail(request, series_id):

    return render(request, 'courses/detail.html')
