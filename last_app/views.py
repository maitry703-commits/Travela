from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import django.contrib.auth as auth   # 👈 aa line very important
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from datetime import datetime
import razorpay
from django.conf import settings

def razorpay_payment(request, type, id):

    if type == "package":
        booking = get_object_or_404(PackageBooking, id=id)
        amount = int(booking.total)

    elif type == "hotel":
        booking = get_object_or_404(HotelBooking, id=id)
        amount = int(booking.total)

    elif type == "flight":
        booking = get_object_or_404(FlightBooking, id=id)
        amount = int(booking.total)

    else:
        return render(request, "error.html")

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        "type": type,
        "booking": booking,
        "payment": payment,
        "key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "display_amount": amount / 100
    }

    return render(request, "razorpay_payment.html", context)
def payment_success(request, type, id):

    if type == "package":
        booking = get_object_or_404(PackageBooking, id=id)

    elif type == "hotel":
        booking = get_object_or_404(HotelBooking, id=id)

    elif type == "flight":
        booking = get_object_or_404(FlightBooking, id=id)

    else:
        return render(request, "error.html", {"message": "Invalid Type"})

    booking.payment_status = True
    booking.save()

    return render(request, "payment_success.html", {
        "booking": booking,
        "type": type
    })# Create your views here.
def index(request):
    herosection_data = HeroSection.objects.all()
    services = Service.objects.all()
    context = {
        "herosection_data" : herosection_data,
        "services": services
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def services(request):
    services = Service.objects.all()
    context = {
        "services" : services
    }
    return render(request, 'services.html', context)


def hotel(request):
    hotels = Hotel.objects.all()
    context = {
        "hotels":hotels
    }
    return render(request, 'hotel.html',context)

def hotel_book(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    context = {
        'hotel':hotel
    }
    return render(request, 'hotel_book.html',context)

def hotel_confirm(request):
    if request.method == "POST":

        hotel = request.POST.get('hotel')
        city = request.POST.get('city')
        price = float(request.POST.get('price'))  # convert to float
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        guests = request.POST.get('guests')

        # Total calculate
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        days = (check_out_date - check_in_date).days
        total = float(price) * days


        # Save Data
        hotel_booking = HotelBooking.objects.create(
            hotel=hotel,
            city=city,
            price=price,
            name=name,
            phone=phone,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            total=total
        
        )

        
        return render(request, "hotel_confirm.html",{'hotel_booking':hotel_booking,'total_days':days})

    return redirect('/')



def flight(request):
    flights = Flight.objects.all()
    context = {
        "flights": flights
    }
    return render(request, "flight.html", context)


def flight_book(request, id):
    flight = get_object_or_404(Flight, id=id)
    context = {
        "flight": flight
    }
    return render(request, "flight_book.html", context)

def flight_confirm(request):
    if request.method == "POST":
        flight_id = request.POST.get("flight_id")
        flight = get_object_or_404(Flight, id=flight_id)

        # # airline = request.POST.get('airline')
        # # from_location = request.POST.get('from_location')
        # # to_location = request.POST.get('to_location')
        # # departure_time= request.POST.get('departure_time')

        # # Safe conversion
        # try:
        #     price = float(request.POST.get('price'))
        # except (TypeError, ValueError):
        #     price = 0.0

        name = request.POST.get('name')
        email=request.POST.get('email')
        phone = request.POST.get('phone')
        travel_date = request.POST.get('travel_date')


        try:
            passengers = int(request.POST.get('passengers'))
        except (TypeError, ValueError):
            passengers = 1

        # ✅ Total Calculate
        total = flight.price * passengers

        # ✅ Save Booking
        flight_booking = FlightBooking.objects.create(
            airline=flight.airline_name,
            from_location=flight.from_location,
            to_location=flight.to_location,
            departure_time=flight.departure_time,   # ADD THIS
            price=flight.price,
            name=name,
            email=email,
            phone=phone,
            travel_date=travel_date,
            passengers=passengers,
            total=total
        )

        return render(request, "flight_confirm.html", {
            "flight_booking": flight_booking,
            "total_amount": total
        })

    return redirect('/')
def blog(request):
    return render(request, 'blog.html')

def booking(request):
    return render(request, 'booking.html')

def booking_confirm(request):
    return render(request, 'booking_confirm.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # same page reload
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def destination(request):
    destination_data= Destination.objects.all()
    usa = Destination.objects.filter(country="USA")
    canada = Destination.objects.filter(country="Canada")
    europe = Destination.objects.filter(country="Europe")
    china = Destination.objects.filter(country="China")
    singapore = Destination.objects.filter(country="Singapore")
    context = {
        "destination_data": destination_data,
        "usa": usa,
        "canada": canada,
        "europe": europe,
        "china": china,
        "singapore": singapore,
    }
    return render(request, 'destination.html',context)

def gallery(request):
    gallery_data = Gallery.objects.all()
    world = Gallery.objects.filter(category="World Tour")
    ocean = Gallery.objects.filter(category="Ocean Tour")
    summer = Gallery.objects.filter(category="Summer Tour")
    adventure = Gallery.objects.filter(category="Adventure Tour")
    mountain = Gallery.objects.filter(category="Mountain Tour")

    context = {
        "gallery_data" : gallery_data,
        'world': world,
        'ocean': ocean,
        'summer': summer,
        'adventure': adventure,
        'mountain': mountain,

    }
    return render(request, 'gallery.html', context)

def guides(request):
    guide_data = Guide.objects.all()
    context = {
        'guide_data' : guide_data
    }
    return render(request, 'guides.html',context)

def testimonial(request):
    testimonial_data = Testimonial.objects.all()
    context = {
        "testimonial_data" : testimonial_data
    }
    return render(request, 'testimonial.html',context)

def tour(request):
    national = TourCategory.objects.filter(category_type="NATIONAL")
    international = TourCategory.objects.filter(category_type="INTERNATIONAL")

    context = {
        "national":national,
        "international":international
    }
    return render(request, 'tour.html', context)

def payment_booking(request):
    return render(request, 'payment_booking.html')

def pay_now(request):
    return render(request, "pay_now.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            mobile = form.cleaned_data['mobile']
            address = form.cleaned_data['address']
            image = form.cleaned_data.get('image')

            user = User.objects.create_user(username=name, email=email, password=password, first_name=name)
            Profile.objects.create(user=user, mobile=mobile, address=address, image=image)

            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')   # 👈 Direct Home Page
        else:
            messages.error(request, "Invalid Email or Password!")

    return render(request, 'login.html')

def logout(request):
    return render(request, 'logout.html')

def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        
        user.first_name = request.POST.get("name")
        user.email = request.POST.get("email")
        user.image = request.POST.get("image")
        user.save()

        return redirect("profile")   # 👈 Save pachi Profile page open thase

    return render(request, "edit_profile.html")
def inbox(request):
    hotel_bookings = HotelBooking.objects.filter(payment_status=True).order_by('-booking_date')
    flight_bookings = FlightBooking.objects.filter(payment_status=True).order_by('-booking_date')
    package_bookings = PackageBooking.objects.filter(payment_status=True).order_by('-booking_date')

    context = {
        'hotel_bookings': hotel_bookings,
        'flight_bookings': flight_bookings,
        'package_bookings': package_bookings,
    }

    return render(request, "inbox.html", context)
def delete_booking(request, type, id):

    if type == "hotel":
        booking = get_object_or_404(HotelBooking, id=id)

    elif type == "flight":
        booking = get_object_or_404(FlightBooking, id=id)

    elif type == "package":
        booking = get_object_or_404(PackageBooking, id=id)

    else:
        return redirect('inbox')

    booking.delete()
    messages.success(request, "Booking deleted successfully!")

    return redirect('inbox')

def notification(request):
    return render(request, 'notification.html')

def error(request):
    return render(request, '404.html')

def packages(request):
    packages = Package.objects.all()
    context = {
        "packages": packages
    }
    return render(request, "packages.html", context)
def package_detail(request, slug):
    package = get_object_or_404(Package, slug=slug)
    return render(request, "package_detail.html", {"package": package})
def package_book(request, id):
    package = get_object_or_404(Package, id=id)
    context = {
        "package": package
    }
    return render(request, "package_book.html", context)

def package_confirm(request):
    if request.method == "POST":
        package_id = request.POST.get('package_id')
        package = Package.objects.get(id=package_id)
        # title = request.POST.get('title')
        # destination = request.POST.get('destination')
        # price = float(request.POST.get('price'))
        # duration_days = int(request.POST.get('duration_days'))
   
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        travel_date = request.POST.get('travel_date')
        persons = int(request.POST.get('persons'))

        # ✅ Total Calculate
        total = package.price * persons

        # ✅ Save Booking
        package_booking = PackageBooking.objects.create(
            package_title=package.title,
            destination=package.destination,
            price=package.price,
            duration_days=package.duration_days,
            name=name,
            email=email,   # 👈 ADD

            phone=phone,
            travel_date=travel_date,
            persons=persons,
            total=total
        )

        return render(request, "package_confirm.html", {
            "package_booking": package_booking,
            "total_amount": total
        })

    return redirect('/')