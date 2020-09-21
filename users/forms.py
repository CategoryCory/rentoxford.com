from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

CustomUserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUserModel
        fields = ('email', 'username', )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUserModel
        fields = ('email', 'username', )
