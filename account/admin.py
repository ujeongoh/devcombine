from django.contrib import admin
from .models import UserProfile

# Register your models here.
admin.site.register(UserProfile)


class AccountAdmin(admin.ModelAdmin):
    change_list_template = 'account/change_list.html'
