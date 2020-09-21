from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUserModel = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUserModel
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_approved', ]
    list_editable = ['is_approved', ]
    list_filter = ['is_approved', ]
    list_per_page = 25
    # fieldsets = ()


admin.site.register(CustomUserModel, CustomUserAdmin)
