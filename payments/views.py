from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from users.forms import PaymentAmountForm


@login_required
def payment_amount(request):
    current_user = request.user

    if request.method == 'POST':
        form = PaymentAmountForm(request.POST)
        if form.is_valid():
            # create payment intent and go to payment page
            pass
        else:
            # redisplay page with form errors
            pass
    else:
        form = PaymentAmountForm()

    return render(request, 'payments/payment_amount.html', {'form': form, 'base_rent': current_user.monthly_rent})


@login_required
def create_payment_intent(request):
    if request.method == 'POST':
        payment_amount_form = PaymentAmountForm(request.POST)
        if payment_amount_form.is_valid():
            amount = payment_amount_form.cleaned_data['amount']
            return HttpResponse('You are paying ' + str(amount))
        else:
            return HttpResponse('There was a problem with the form!')
    else:
        return redirect('pages:home')
