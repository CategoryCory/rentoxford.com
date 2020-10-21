from django.contrib import admin

from .models import Company, Lease, LeaseDocument, LeaseCharge, LeasePayment


class LeaseDocumentInline(admin.TabularInline):
    model = LeaseDocument
    extra = 3


class LeaseAdmin(admin.ModelAdmin):
    list_display = ['property', 'company', 'lease_begin', 'lease_end', 'monthly_rent', ]
    search_fields = ['property', 'company', ]
    list_per_page = 25
    inlines = [
        LeaseDocumentInline,
    ]


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'street_address', 'city', 'state', 'zip_code', ]
    list_per_page = 25


class LeaseChargeAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'due_date', 'amount', 'balance', 'status', 'notes', ]
    list_filter = ['tenant', 'due_date', ]
    list_per_page = 25


class LeasePaymentAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'date', 'amount', 'balance', 'notes', ]
    list_filter = ['tenant', ]
    list_per_page = 25


admin.site.register(Lease, LeaseAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(LeaseCharge, LeaseChargeAdmin)
admin.site.register(LeasePayment, LeasePaymentAdmin)
