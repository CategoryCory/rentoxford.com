from django.db import models
from django.utils import timezone

from listings.models import Listing


class Company(models.Model):
    company_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=25, blank=True)
    zip_code = models.CharField(max_length=25, blank=True)
    phone_number = models.CharField(max_length=25, blank=True)
    contact_email = models.EmailField(max_length=50, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = 'Companies'


class Lease(models.Model):
    property = models.ForeignKey(Listing, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    lease_begin = models.DateField(default=timezone.now)
    lease_end = models.DateField(default=timezone.now)
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    initial_payment = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.property}: {self.lease_begin} - {self.lease_end}'


class LeaseDocument(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    lease_document = models.FileField(upload_to='documents/%Y/%m/%d/', verbose_name='Lease Document')

    class Meta:
        verbose_name = 'Lease Document'
        verbose_name_plural = 'Lease Documents'

    def __str__(self):
        return f'{self.lease} - {self.description}'
