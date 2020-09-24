from django.contrib import admin

from .models import Listing, ListingGalleryImages


class ImageInline(admin.TabularInline):
    model = ListingGalleryImages
    extra = 3


class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'monthly_rent', 'availability', ]
    list_editable = ['availability', ]
    search_fields = ['title', 'description', ]
    list_per_page = 25
    prepopulated_fields = {'slug': ('title', )}
    inlines = [
        ImageInline,
    ]


admin.site.register(Listing, ListingAdmin)
