from django.views.generic import FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import PaymentAmountForm

CustomUser = get_user_model()


class UserDashboardView(LoginRequiredMixin, FormView):
    model = CustomUser
    template_name = 'users/user_dashboard.html'
    form_class = PaymentAmountForm
    # success_url = reverse_lazy('payments:create_payment_intent')
