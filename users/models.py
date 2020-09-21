from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(default=timezone.now)
    is_approved = models.BooleanField(verbose_name='Approved',
                                      help_text='Designates whether this user has been approved.',
                                      default=False)
    address_street = models.CharField(verbose_name='Street Address', max_length=200)
    address_city = models.CharField(verbose_name='City', max_length=75)
    address_state = models.CharField(verbose_name='State', max_length=50)
    address_zip = models.CharField(verbose_name='ZIP Code', max_length=50)

    def __str__(self):
        return self.username
