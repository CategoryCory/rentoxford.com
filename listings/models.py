from django.db import models
from datetime import datetime
from django.urls import reverse


class Listing(models.Model):
    AVAILABLE = 'available'
    RENTED = 'rented'

    AVAILABILITY_CHOICES = (
        (AVAILABLE, 'Available'),
        (RENTED, 'Rented'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    monthly_rent = models.DecimalField(verbose_name='Monthly Rent', default=0, max_digits=8, decimal_places=2)
    security_deposit = models.DecimalField(verbose_name='Security Deposit', default=0, max_digits=8, decimal_places=2)
    street_address = models.CharField(verbose_name='Street Address', max_length=200)
    city = models.CharField(verbose_name='City', max_length=100)
    state = models.CharField(verbose_name='State', max_length=100)
    zipcode = models.CharField(verbose_name='ZIP Code', max_length=20)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.FloatField(default=0)
    has_garage = models.BooleanField(default=False)
    square_feet = models.IntegerField(default=0)
    cats_allowed = models.BooleanField(verbose_name='Are cats allowed?', default=False)
    dogs_allowed = models.BooleanField(verbose_name='Are dogs allowed?', default=False)
    is_published = models.BooleanField(verbose_name='Is published?',
                                       help_text='If not checked, this property will not appear on the site.',
                                       default=False)
    availability = models.CharField(max_length=30, choices=AVAILABILITY_CHOICES, default=AVAILABLE)
    available_date = models.DateTimeField(verbose_name='Date of availability',
                                          help_text='Indicates when this property will become available to rent.',
                                          default=datetime.now,
                                          blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    main_image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    gallery_image_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    gallery_image_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    gallery_image_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    gallery_image_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    gallery_image_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    gallery_image_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listing_detail', kwargs={'slug': self.slug})
