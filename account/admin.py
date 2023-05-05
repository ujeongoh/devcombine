from django.contrib import admin
from .models import UserProfile
from .forms import CSVUploadForm

# Register your models here.


@admin.register(UserProfile)
class AccountAdmin(admin.ModelAdmin):
    # list_display = ('id', 'title', 'instructor', 'site', 'price')

    change_list_template = 'admin/account/account/course_change_list.html'
