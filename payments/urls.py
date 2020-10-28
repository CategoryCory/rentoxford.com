from django.urls import path

from . import views

app_name = 'payments'
urlpatterns = [
    path('payment-amount/', views.payment_amount, name='payment_amount'),
    path('make-payment/<amt>/', views.make_payment, name='make_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('get-payment-intent/', views.get_payment_intent, name='get_payment_intent'),
]
