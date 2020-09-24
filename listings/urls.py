from django.urls import path

from .views import ListingListView, ListingDetailView

app_name = 'listings'
urlpatterns = [
    path('', ListingListView.as_view(), name='listing_list'),
    path('<slug:slug>/', ListingDetailView.as_view(), name='listing_detail'),
]