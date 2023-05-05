from django.contrib import admin
from django.urls import path, include
import account.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('series/', include('series.urls')),
    path('account/', include('account.urls')),

    # 리팩토링
    path('signup', account.views.signup_view, name='signup'),
    path('login', account.views.login_view, name='login'),
    path('logout', account.views.logout_view, name='logout'),
    path('get-csrf-token/', account.views.get_csrf_token, name='get_csrf_token'),
]
