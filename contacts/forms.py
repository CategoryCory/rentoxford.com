from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Contact


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('name', 'email_address', 'phone_number', 'message', )
        labels = {
            'name': _('What is your name?'),
            'email_address': _('Please enter your email address.'),
            'phone_number': _('Please enter a phone number where you can be reached (optional).'),
            'message': _('How can we help you?'),
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, })
        }
