from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('login-success/', views.login_success, name='login_success'),
    path('dashboard/', views.UserDashboardView.as_view(), name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/tenants/', views.admin_dashboard_tenants, name='admin_dashboard_tenants'),
    path('submit-maintenance-request/', views.SubmitMaintenanceRequestView.as_view(), name='submit_maintenance_request'),
]