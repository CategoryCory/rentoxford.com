from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from listings.models import Listing


@login_required
def ad_home(request):
    if request.user.is_staff is False:
        return redirect('pages:home')
    else:
        listings = Listing.objects.all()
        context = {
            'listings': listings
        }
        return render(request, 'admin_dashboard/ad_home.html', context)


@login_required
def ad_tenants(request):
    if request.user.is_staff is False:
        return redirect('pages:home')
    else:
        return render(request, 'admin_dashboard/ad_tenants.html')
