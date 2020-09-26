from django.urls import path

from .views import UserDashboardView

app_name = 'users'
urlpatterns = [
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
]