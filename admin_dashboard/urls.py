from django.urls import path

from . import views

app_name = 'admin_dashboard'
urlpatterns = [
    path('', views.ad_home, name='ad_home'),
    path('tenants/', views.ad_tenants, name='ad_tenants'),
    path('tenants/<int:tenant_id>/add-payment/', views.AddTenantPaymentView.as_view(), name='ad_add_tenant_payment'),
]