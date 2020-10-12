from django.views.generic import ListView, DetailView
from django.conf import settings
from django.db.models import Q

from .models import Listing


class ListingListView(ListView):

    model = Listing
    paginate_by = 10

    search_values = {}

    def get_search_values(self):
        num_bedrooms = self.request.GET.get('numBedrooms')
        min_cost = self.request.GET.get('minCost')
        max_cost = self.request.GET.get('maxCost')
        school_district = self.request.GET.get('schoolDistrict')
        allows_pets = self.request.GET.get('allowsPets')
        fenced_yard = self.request.GET.get('fencedYard')

        has_errors = False

        self.search_values['num_bedrooms'] = num_bedrooms
        self.search_values['min_cost'] = min_cost
        self.search_values['max_cost'] = max_cost
        self.search_values['school_district'] = school_district
        self.search_values['allows_pets'] = allows_pets
        self.search_values['fenced_yard'] = fenced_yard

    def get_queryset(self):
        self.get_search_values()
        queryset = Listing.objects.filter(is_published=True).order_by('available_date')

        if self.search_values['num_bedrooms']:
            queryset = queryset.filter(bedrooms__lte=self.search_values['num_bedrooms'])

        if self.search_values['min_cost']:
            queryset = queryset.filter(monthly_rent__gte=self.search_values['min_cost'])

        if self.search_values['max_cost']:
            queryset = queryset.filter(monthly_rent__lte=self.search_values['max_cost'])

        if self.search_values['school_district'] and self.search_values['school_district'] != 'any':
            queryset = queryset.filter(school_district__iexact=self.search_values['school_district'])

        if self.search_values['allows_pets'] == 'yes':
            queryset = queryset.filter(Q(cats_allowed=True) | Q(dogs_allowed=True))

        if self.search_values['fenced_yard'] == 'yes':
            queryset = queryset.filter(has_fence=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maps_api_key'] = settings.MAPS_API_KEY
        context['school_districts'] = Listing.SCHOOL_CHOICES
        context['search_values'] = self.search_values
        return context


class ListingDetailView(DetailView):

    model = Listing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_images_range'] = range(self.get_object().listinggalleryimages_set.all().count())
        context['maps_api_key'] = settings.MAPS_API_KEY
        return context
