from django.contrib import admin

from .models import Lease


class LeaseAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'property', 'lease_begin', 'lease_end', 'monthly_rent', ]
    search_fields = ['tenant', 'property', ]
    list_per_page = 25


admin.site.register(Lease, LeaseAdmin)
