from django.views.generic import ListView, DetailView
from django.conf import settings

from .models import Listing


class ListingListView(ListView):

    model = Listing
    paginate_by = 6
    ordering = ['-created_on', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maps_api_key'] = settings.MAPS_API_KEY
        return context


class ListingDetailView(DetailView):

    model = Listing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_images_range'] = range(self.get_object().listinggalleryimages_set.all().count())
        context['maps_api_key'] = settings.MAPS_API_KEY
        return context
