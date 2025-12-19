from django.shortcuts import render
from django.db.models import Q
from venues.models import Venue
from .forms import SearchForm

def home(request):
    featured_venues = Venue.objects.filter(status=Venue.Status.ACTIVE)[:3]
    return render(request, 'core/home.html', {'featured_venues': featured_venues})

def search(request):
    form = SearchForm(request.GET)
    venues = Venue.objects.filter(status=Venue.Status.ACTIVE)

    if form.is_valid():
        query = form.cleaned_data.get('query')
        venue_type = form.cleaned_data.get('venue_type')
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')
        capacity = form.cleaned_data.get('capacity')

        if query:
            venues = venues.filter(name__icontains=query)
        if venue_type:
            venues = venues.filter(venue_type=venue_type)
        if price_min:
            venues = venues.filter(base_price__gte=price_min)
        if price_max:
            venues = venues.filter(base_price__lte=price_max)
        if capacity:
            venues = venues.filter(capacity__gte=capacity)

    return render(request, 'core/search.html', {'form': form, 'venues': venues})
