from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from listings.models import Listing


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(default=timezone.now)
    is_approved = models.BooleanField(verbose_name='Approved',
                                      help_text='Designates whether this user has been approved.',
                                      default=False)
    property = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, blank=True)
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.username
