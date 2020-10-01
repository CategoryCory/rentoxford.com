from django.views.generic import TemplateView, CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from maintenance_requests.models import MaintenanceRequest

CustomUser = get_user_model()


class UserDashboardView(LoginRequiredMixin, TemplateView):
    model = CustomUser
    template_name = 'users/user_dashboard.html'


class SubmitMaintenanceRequestView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = MaintenanceRequest
    template_name = 'users/submit-maintenance-request.html'
    fields = ('description', )
    success_url = reverse_lazy('users:user_dashboard')
    success_message = 'Your maintenance request has been submitted! We will be in touch with you shortly.'

    def form_valid(self, form):
        form.instance.tenant = self.request.user
        return super().form_valid(form)
