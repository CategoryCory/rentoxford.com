from django.contrib import admin

from .models import Company, Lease, LeaseDocument


class LeaseDocumentInline(admin.TabularInline):
    model = LeaseDocument
    extra = 3


class LeaseAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'property', 'lease_begin', 'lease_end', 'monthly_rent', ]
    search_fields = ['tenant', 'property', ]
    list_per_page = 25
    inlines = [
        LeaseDocumentInline,
    ]


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'street_address', 'city', 'state', 'zip_code', ]
    list_per_page = 25


admin.site.register(Lease, LeaseAdmin)
admin.site.register(Company, CompanyAdmin)
