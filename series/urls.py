from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'series'

urlpatterns = [
    path('', views.SeriesListView.as_view(), name='main_series'),
    path('list/', views.SeriesListView.as_view(), name='total_seires'),
    path('<int:series_id>/', views.SereisCourseListView.as_view(), name='series_course')
]
