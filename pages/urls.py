from django.urls import path

from .views import HomePageView, ContactPageView, CommunitiesPageView

app_name = 'pages'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('communities/', CommunitiesPageView.as_view(), name='communities'),
]