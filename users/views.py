from django.views.generic import TemplateView, CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from datetime import datetime

from maintenance_requests.models import MaintenanceRequest
from transactions.models import Charge, Payment

CustomUser = get_user_model()


@login_required
def login_success(request):
    if request.user.is_staff is True:
        return redirect('admin_dashboard:ad_home')
    else:
        return redirect('users:user_dashboard')


class UserDashboardView(LoginRequiredMixin, TemplateView):
    model = CustomUser
    template_name = 'users/user_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.today().date()
        maintenance_requests = MaintenanceRequest.objects.filter(tenant=self.request.user)
        current_lease = self.request.user.lease
        active_charges = Charge.objects.filter(
            tenant=self.request.user,
            balance__gt=0
        ).order_by('due_date')
        payments = Payment.objects.filter(
            tenant=self.request.user
        ).order_by('-date')
        context['maintenance_requests'] = maintenance_requests
        context['current_lease'] = current_lease
        context['active_charges'] = active_charges
        context['payments'] = payments
        context['total_due'] = sum(chrg.balance for chrg in active_charges if chrg.due_date <= today)
        context['total_charges'] = sum(chrg.balance for chrg in active_charges)
        if self.request.user.rent_amount > 0:
            context['rent_display'] = self.request.user.rent_amount
        return context


class SubmitMaintenanceRequestView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = MaintenanceRequest
    template_name = 'users/submit-maintenance-request.html'
    fields = ('description', )
    success_url = reverse_lazy('users:user_dashboard')
    success_message = 'Your maintenance request has been submitted! We will be in touch with you shortly.'

    def test_func(self):
        return self.request.user.is_approved is True

    def form_valid(self, form):
        form.instance.tenant = self.request.user
        email_subject = 'New RentOxford maintenance request'
        email_body = (
            f'There has been a maintenance request submitted on RentOxford.com.\n'
            f'Tenant: {self.request.user.first_name} {self.request.user.last_name}\n'
            f'Tenant Email: {self.request.user.email}\n'
            f'Description: {form.cleaned_data.get("description")}'
        )
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.SEND_ADMIN_EMAIL_TO],
            fail_silently=True
        )
        return super().form_valid(form)
