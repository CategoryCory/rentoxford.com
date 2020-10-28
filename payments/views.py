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
    print('Set payment amount')
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
    payment_id = request.GET.get('p')
    payment_conf = request.GET.get('p_cnf')
    amount = request.GET.get('amt')

    if not payment_id or not payment_conf or not amount:
        return redirect('pages:home')
    else:
        indx = payment_conf.rfind('-')
        tstamp = payment_conf[:indx]
        payment_date = datetime.fromtimestamp(int(tstamp))
        amount_dec = Decimal(amount) / Decimal(100)

        pmt = Payment(
            tenant=request.user,
            amount=amount_dec,
            balance=amount_dec,
            stripe_payment_id=payment_id,
        )

        pmt.save()

        current_charges = Charge.objects.filter(tenant=request.user, balance__gt=0).order_by('due_date')

        for chrg in current_charges:
            if pmt.balance <= 0:
                break

            if pmt.balance >= chrg.balance:
                pmt.balance -= chrg.balance
                chrg.balance = 0
                chrg.status = Charge.PAID
            else:
                chrg.balance -= pmt.balance
                pmt.balance = 0

            pmt.notes += f'{chrg.type} due on {chrg.due_date}; '
            pmt.charges.add(chrg)
            pmt.save()
            chrg.save()

        context = {
            'pmt_conf': payment_conf,
            'pmt_time': payment_date.strftime('%b %d %Y %H:%M:%S'),
            'amount': int(amount) / 100.0,
            'name': request.user,
            'property': request.user.lease.property
        }
        return render(request, 'payments/payment_success.html', context)


@login_required
def get_payment_intent(request):
    if request.method == 'POST':
        try:
            print('Method was post')
            stripe_sk = StripeKey.objects.filter(
                company=request.user.lease.company
            ).values('stripe_secret_key')[0]['stripe_secret_key']
            stripe.api_key = stripe_sk
            if stripe_sk:
                print('Found')
            data = json.loads(request.body)
            print('Data found')
            intent = stripe.PaymentIntent.create(
                amount=data['payment_amount'],
                currency='usd',
                metadata={'description': data['description']},
            )
            print('Intent created')

            return JsonResponse({
                'clientSecret': intent['client_secret']
            })

        except Exception as e:
            return JsonResponse(error=str(e))
    else:
        return redirect('pages:home')
