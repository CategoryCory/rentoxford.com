from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from listings.models import Listing
UserModel = get_user_model()


class Lease(models.Model):
    tenant = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    property = models.ForeignKey(Listing, on_delete=models.CASCADE)
    lease_begin = models.DateField(default=timezone.now)
    lease_end = models.DateField(default=timezone.now)
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    initial_payment = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.tenant.first_name} {self.tenant.last_name}: {self.lease_begin}-{self.lease_end}'
