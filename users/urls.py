from django.urls import path

from .views import login_success, admin_dashboard, UserDashboardView, SubmitMaintenanceRequestView

app_name = 'users'
urlpatterns = [
    path('login-success/', login_success, name='login_success'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('submit-maintenance-request/', SubmitMaintenanceRequestView.as_view(), name='submit_maintenance_request'),
]