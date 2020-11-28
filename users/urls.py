from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('login-success/', views.login_success, name='login_success'),
    path('dashboard/', views.UserDashboardView.as_view(), name='user_dashboard'),
    path('submit-maintenance-request/',
         views.SubmitMaintenanceRequestView.as_view(),
         name='submit_maintenance_request'),
]