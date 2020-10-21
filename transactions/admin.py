from django.contrib import admin

from .models import Charge, Payment


class ChargeAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'due_date', 'amount', 'balance', 'status', 'notes', ]
    list_filter = ['tenant', 'due_date', ]
    list_per_page = 25


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'date', 'amount', 'balance', 'notes', ]
    list_filter = ['tenant', ]
    list_per_page = 25


admin.site.register(Charge, ChargeAdmin)
admin.site.register(Payment, PaymentAdmin)
