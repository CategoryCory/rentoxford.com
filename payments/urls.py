from django.urls import path

from . import views

app_name = 'payments'
urlpatterns = [
    path('payment-amount/', views.payment_amount, name='payment_amount'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
]
