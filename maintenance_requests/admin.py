from django.contrib import admin

from .models import MaintenanceRequest


class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'status', 'created_on', ]
    list_editable = ['status', ]
    list_filter = ['status', ]
    list_per_page = 25


admin.site.register(MaintenanceRequest, MaintenanceRequestAdmin)
