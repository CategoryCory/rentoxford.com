from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email_address', 'created_on', ]
    list_per_page = 25


admin.site.register(Contact, ContactAdmin)
