from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from listings.models import Listing


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(default=timezone.now)
    is_approved = models.BooleanField(verbose_name='Approved',
                                      help_text='Designates whether this user has been approved.',
                                      default=False)

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.username
