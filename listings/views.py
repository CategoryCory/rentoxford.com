from django.views.generic import ListView, DetailView

from .models import Listing


class ListingListView(ListView):

    model = Listing


class ListingDetailView(DetailView):

    model = Listing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_images_range'] = range(self.get_object().listinggalleryimages_set.all().count())
        return context
