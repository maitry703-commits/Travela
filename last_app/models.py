from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
# 1.Herosection model
class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    background_image = models.ImageField(upload_to="hero/")
    button_text = models.CharField(max_length=100)
    button_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
# 2.Service model
class Service(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_class = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# 3.Destination model
class Destination(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    country = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="destinations/")
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

# 4.TourCategory model
CATEGORY_TYPE = (
    ('NATIONAL', 'National'),
    ('INTERNATIONAL', 'International'),
)
class TourCategory(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE)
    image = models.ImageField(upload_to="tour_categories/")

    def __str__(self):
        return f"{self.name} ({self.category_type})"

# 5.package model
class Package(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="packages")
    category = models.ForeignKey(TourCategory, on_delete=models.CASCADE, related_name="packages")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to="packages/")
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class PackageBooking(models.Model):

    package_title = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()

    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)   # 👈 ADD THIS

    phone = models.CharField(max_length=15)

    travel_date = models.DateField()
    persons = models.IntegerField()

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.package_title}"

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='hotels/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class HotelBooking(models.Model):
    
    hotel = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)

    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    total = models.IntegerField(default=0)

    payment_status = models.BooleanField(default=False)

    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.hotel}"


# 6.gallery model
class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="gallery/")
    category = models.CharField(max_length=100, blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
# 7.guide model
class Guide(models.Model):
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    bio = models.TextField()
    image = models.ImageField(upload_to="guides/")
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
# 8.blog model
class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="blogs/")
    content = models.TextField()
    author = models.CharField(max_length=150)
    published_at = models.DateTimeField()
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
# 9.testimonial model
class Testimonial(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="testimonials/")
    message = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.rating}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Flight(models.Model):
    airline_name = models.CharField(max_length=100)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    departure_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='flights/')

class FlightBooking(models.Model):

    airline = models.CharField(max_length=200)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    departure_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    name = models.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)   # ✅ ADD THIS

    phone = models.CharField(max_length=15)

    travel_date = models.DateField()
    passengers = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.airline}"