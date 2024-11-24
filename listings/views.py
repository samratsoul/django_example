from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from listings.choices import price_choices, bedroom_choices, state_choices

from .models import Listings


def index(request):
    listings = Listings.objects.order_by('-list_date')
    paginator = Paginator(listings, 3) 
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings' : paged_listings,
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):

    listing = get_object_or_404(Listings, pk=listing_id)
    context = {
        'listing' : listing
    }
    return render(request, 'listings/listing.html', context)

def search(request):
    query_set_list = Listings.objects.order_by('-list_date')

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            query_set_list = query_set_list.filter(description__icontains= keywords)
    

    

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            query_set_list = query_set_list.filter(city__iexact= city)
    

    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            query_set_list = query_set_list.filter(state__iexact= state)
    

    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            query_set_list = query_set_list.filter(bedrooms__lte= bedrooms)
    


    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            query_set_list = query_set_list.filter(price__lte= price)
    

    context = {
        'price_choices' : price_choices,
        'bedroom_choices' : bedroom_choices,
        'state_choices' : state_choices,
        'listings': query_set_list,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)
