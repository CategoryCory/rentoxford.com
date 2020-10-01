from django.urls import path

from .views import UserDashboardView, SubmitMaintenanceRequestView

app_name = 'users'
urlpatterns = [
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('submit-maintenance-request/', SubmitMaintenanceRequestView.as_view(), name='submit_maintenance_request'),
]