from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from listings.models import Listing
CustomUser = get_user_model()


@login_required
def ad_home(request):
    if not request.user.is_staff:
        return redirect('pages:home')
    else:
        listings = Listing.objects.all()
        context = {
            'listings': listings
        }
        return render(request, 'admin_dashboard/ad_home.html', context)


@login_required
def ad_tenants(request):
    if not request.user.is_staff:
        return redirect('pages:home')
    else:
        tenants = CustomUser.objects.filter(is_staff=False)
        context = {
            'tenants': tenants
        }
        return render(request, 'admin_dashboard/ad_tenants.html', context)
