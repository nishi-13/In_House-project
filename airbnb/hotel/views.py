from django.shortcuts import render, redirect
from .models import Hotel, Location, Booking, Reviews

# Create your views here.
def get_location_detials(request, location_name): # api
    location = Location.objects.get(name__iexact=location_name) # sql query
    if not location:
        return {
            "error": "location not found",
            "status_code": 200
        }
    hotels = Hotel.objects.filter(location__name__iexact=location_name)
    context = {
        "location": location,
        "hotels": hotels
    }
    return render(request, "hotel/location_details.html", context=context)

def get_location_detials_by_name(request):
    kwargs = dict(request.GET)
    print(kwargs.get("city")[0])
    location = Location.objects.get(name__iexact=kwargs.get("city")[0])
    hotels = Hotel.objects.filter(location__name__iexact=kwargs.get("city")[0])
    context = {
        "location": location,
        "hotels": hotels
    }
    return render(request, "hotel/location_details.html", context=context)

def get_hotel_detials(request, hotel_name):
    hotel = Hotel.objects.get(name__iexact=hotel_name)
    location_name = hotel.location.name
    related_hotels = Hotel.objects.filter(location__name=location_name).exclude(name__iexact=hotel_name)
    reviews = Reviews.objects.filter(hotel=hotel)
    context = {
        "hotel": hotel,
        "location_name": location_name,
        "hotels": related_hotels,
        "reviews": reviews
    }
    return render(request, "hotel/hotel_details.html", context=context)


def book(request, pk):
    if request.method == 'POST':
        guest = request.POST['guest']
        days = request.POST['days']
        hotel = Hotel.objects.get(id=pk)
        total = int(hotel.price) * int(days)
        Booking.objects.create(user=request.user, hotel=hotel, guest=guest, days=days, total=total)
        return redirect('profile')
    return redirect('index')

def cancel(request, pk):
    Booking.objects.filter(id=pk).delete()
    return redirect('profile')

def review(request, pk):
    if request.method == 'POST':
        text = request.POST['text']
        hotel = Hotel.objects.get(id=pk)
        Reviews.objects.create(hotel=hotel, text=text, user=request.user)
    return redirect('get_hotel_detials')