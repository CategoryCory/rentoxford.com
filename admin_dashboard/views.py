from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from transactions.models import Payment
from listings.models import Listing
from . import forms

CustomUser = get_user_model()


class RedirectIfNotStaffMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('pages:home')
        return super(RedirectIfNotStaffMixin, self).dispatch(request, *args, **kwargs)


@login_required
def ad_home(request):
    if not request.user.is_staff:
        return redirect('pages:home')
    else:
        listings = Listing.objects.all()
        context = {
            'listings': listings
        }
        return render(request, 'admin_dashboard/ad_home.html', context)


@login_required
def ad_tenants(request):
    if not request.user.is_staff:
        return redirect('pages:home')
    else:
        tenants = CustomUser.objects.filter(is_staff=False)
        context = {
            'tenants': tenants
        }
        return render(request, 'admin_dashboard/ad_tenants.html', context)


class AddTenantPaymentView(LoginRequiredMixin, RedirectIfNotStaffMixin, SuccessMessageMixin, CreateView):
    model = Payment
    form_class = forms.AddPaymentForm
    template_name = 'admin_dashboard/ad_add_tenant_payment.html'
    success_url = reverse_lazy('admin_dashboard:ad_tenants')
    success_message = 'The payment has been successfully recorded.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_tenant = CustomUser.objects.get(pk=self.kwargs['tenant_id'])
        context['tenant_name'] = f'{current_tenant.first_name} {current_tenant.last_name}'
        return context

    def form_valid(self, form):
        current_tenant = CustomUser.objects.get(pk=self.kwargs['tenant_id'])
        form.instance.tenant = current_tenant
        form.instance.balance = form.instance.amount
        form.instance.type = Payment.OFFLINE
        form.instance.stripe_payment_id = None
        return super().form_valid(form)
