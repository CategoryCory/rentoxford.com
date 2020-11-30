from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime
from decimal import Decimal
import json
import stripe


from transactions.models import Charge, Payment
from leases.models import StripeKey
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
    stripe_pk = StripeKey.objects.filter(
        company=request.user.lease.company
    ).values('stripe_publishable_key')[0]['stripe_publishable_key']
    context = {
        'page_data': {
            'amt': amt,
            'stripe_pk': stripe_pk,
            'name': f'{request.user.first_name} {request.user.last_name}',
            'email': request.user.email,
            'phone': request.user.phone_number,
            'address': request.user.lease.property.full_address,
            'street_address': request.user.lease.property.street_address,
            'city': request.user.lease.property.city,
            'state': request.user.lease.property.state,
            'zipcode': request.user.lease.property.zipcode
        }
    }
    return render(request, 'payments/make_payment.html', context)


@login_required
def payment_success(request):
    payment_conf = request.GET.get('cnf')
    payment_error = request.GET.get('error')

    if not payment_conf and not payment_error:
        return redirect('pages:home')
    else:
        if not payment_error:
            # Retrieve payment by confirmation
            pmt = Payment.objects.filter(confirmation=payment_conf).first()

            # Send error if payment doesn't exist
            if pmt is None:
                context = {
                    'pmt_error': 'This payment does not exist.'
                }
            else:
                context = {
                    'pmt_conf': pmt.confirmation,
                    'pmt_time': pmt.date,
                    'amount': pmt.amount,
                    'name': request.user,
                    'property': request.user.lease.property
                }
        else:
            # Send error
            context = {
                'pmt_error': 'An error occurred while processing this payment.'
            }
        return render(request, 'payments/payment_success.html', context)


@login_required
def record_payment_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            success = True
            error_msg = ''

            # Check to see if a payment with this Stripe id already exists
            pmt = Payment.objects.filter(tenant=request.user, stripe_payment_id=data['pid'])

            # Only save if pmt was not found above
            if not pmt:
                pmt_amount = Decimal(data['amt']) / Decimal(100)

                pmt = Payment(
                    tenant=request.user,
                    amount=pmt_amount,
                    balance=pmt_amount,
                    stripe_payment_id=data['pid'],
                    confirmation=data['conf'],
                )
                pmt.save()
            else:
                success = False
                error_msg = 'Payment already exists'

            return JsonResponse({
                'success': success,
                'error_msg': error_msg
            })

        except Exception as e:
            print(str(e), flush=True)
            return JsonResponse({
                'success': False,
                'error_msg': str(e)
            })
    else:
        return redirect('pages:home')


@login_required
def get_payment_intent(request):
    if request.method == 'POST':
        try:
            stripe_sk = StripeKey.objects.filter(
                company=request.user.lease.company
            ).values('stripe_secret_key')[0]['stripe_secret_key']
            stripe.api_key = stripe_sk
            data = json.loads(request.body)
            intent = stripe.PaymentIntent.create(
                amount=data['payment_amount'],
                currency='usd',
                metadata={'description': data['description']},
            )

            return JsonResponse({
                'clientSecret': intent['client_secret']
            })

        except Exception as e:
            print(str(e), flush=True)
            return JsonResponse(error=str(e))
    else:
        return redirect('pages:home')
