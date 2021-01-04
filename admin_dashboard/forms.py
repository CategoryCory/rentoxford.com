from django import forms

from transactions.models import Payment


class AddPaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['amount', 'date', 'notes', ]
        widgets = {
            'date': forms.DateTimeInput(attrs={
                'id': 'add-payment-datepicker',
            })
        }
