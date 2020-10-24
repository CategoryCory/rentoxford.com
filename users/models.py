from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from listings.models import Listing
from leases.models import Lease


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(default=timezone.now)
    phone_number = models.CharField(max_length=30, blank=True)
    lease = models.ForeignKey(Lease, on_delete=models.SET_NULL, null=True, blank=True)
    rent_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_approved = models.BooleanField(verbose_name='Approved',
                                      help_text='Designates whether this user has been approved.',
                                      default=False)

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.username
