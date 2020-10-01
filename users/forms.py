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
    field_order = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


# TODO: this needs to be moved to the Payments app
class PaymentAmountForm(forms.Form):
    amount = forms.DecimalField(label='Please specify the amount you\'d like to pay', required=True, min_value=0.01)
