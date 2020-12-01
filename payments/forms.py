from django import forms


class PaymentAmountForm(forms.Form):
    amount = forms.DecimalField(label='Please specify the amount you\'d like to pay',
                                required=True,
                                min_value=0.01,
                                widget=forms.NumberInput(attrs={'readonly': 'readonly'}))
