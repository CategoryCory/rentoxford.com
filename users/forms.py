from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from allauth.account.forms import SignupForm as AllauthSignupForm

CustomUserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUserModel
        fields = ('email', 'username', )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUserModel
        fields = ('email', 'username', )


class CustomAllauthUserCreationForm(AllauthSignupForm, forms.Form):
    first_name = forms.CharField(max_length=30,
                                 label='First Name',
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
                                 error_messages={'required': 'You must provide your first name.'})
    last_name = forms.CharField(max_length=30,
                                label='Last Name',
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
                                error_messages={'required': 'You must provide your last name.'})
    phone_number = forms.CharField(max_length=30,
                                   label='Phone Number',
                                   required=True,
                                   widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}),
                                   error_messages={'required': 'You must provide your phone number.'})
    field_order = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

    def save(self, request):
        user = super(CustomAllauthUserCreationForm, self).save(request)
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user
