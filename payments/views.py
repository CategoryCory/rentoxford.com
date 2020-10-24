from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime
import json
import stripe


from transactions.models import Charge
from .forms import PaymentAmountForm


@login_required
def payment_amount(request):
    current_user = request.user
    today = datetime.today()
    current_charges = Charge.objects.filter(tenant=current_user, due_date__lte=today, balance__gt=0)
    total_owed = sum(chrg.balance for chrg in current_charges)

    if request.method == 'POST':
        form = PaymentAmountForm(request.POST)
        if form.is_valid():
            # redirect to payment page with amount
            amt = form.cleaned_data.get('amount')
            return redirect('payments:make_payment', amt=amt)
            pass
        else:
            # redisplay page with form errors
            messages.add_message(
                request,
                messages.ERROR,
                'Please check the form and correct any errors. The amount must be greater than zero.'
            )
    else:
        # Not a POST, so create blank form and display it
        form = PaymentAmountForm()

    return render(request, 'payments/payment_amount.html', {'form': form, 'total_owed': total_owed})


@login_required
def make_payment(request, amt):
    context = {
        'amt': amt,
        'stripe_pk': settings.STRIPE_API_PUBLIC_KEY,
        'name': f'{request.user.first_name} {request.user.last_name}',
        'address': request.user.lease.property
    }
    return render(request, 'payments/make_payment.html', context)


@login_required
def get_payment_intent(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_API_SECRET_KEY
        try:
            data = json.loads(request.body)
            intent = stripe.PaymentIntent.create(
                amount=data['payment_amount'],
                currency='usd',
            )

            return JsonResponse({
                'clientSecret': intent['client_secret']
            })

        except Exception as e:
            return JsonResponse(error=str(e))
    else:
        return redirect('pages:home')
