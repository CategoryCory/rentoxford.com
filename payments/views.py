from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse

from users.forms import PaymentAmountForm


@login_required
def payment_amount(request):
    current_user = request.user

    if request.method == 'POST':
        form = PaymentAmountForm(request.POST)
        if form.is_valid():
            # redirect to payment page with amount
            pass
        else:
            # redisplay page with form errors
            messages.add_message(
                request,
                messages.ERROR,
                'Please check the form and correct any errors. The amount must be a number greater than zero.'
            )
    else:
        # Not a POST, so create blank form and display it
        form = PaymentAmountForm()

    return render(request, 'payments/payment_amount.html', {'form': form, 'base_rent': current_user.monthly_rent})
