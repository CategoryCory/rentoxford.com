from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

CustomUser = get_user_model()


class UserDashboardView(LoginRequiredMixin, TemplateView):
    model = CustomUser
    template_name = 'users/user_dashboard.html'
