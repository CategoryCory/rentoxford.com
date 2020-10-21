from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from calendar import monthrange
import datetime

from listings.models import Listing
UserModel = get_user_model()


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


class LeaseCharge(models.Model):
    DUE = 'due'
    PAID = 'paid'
    LATE = 'late'

    STATUS_CHOICES = (
        (DUE, 'Due'),
        (PAID, 'Paid'),
        (LATE, 'Late'),
    )

    tenant = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    due_date = models.DateField(default=timezone.now)
    amount = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=DUE)
    parent_charge = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Lease Charge'
        verbose_name_plural = 'Lease Charges'

    def __str__(self):
        return f'{self.tenant.first_name} {self.tenant.last_name} - {self.due_date}'


class LeasePayment(models.Model):
    tenant = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    notes = models.CharField(max_length=255, blank=True)
    charges = models.ManyToManyField(LeaseCharge, related_name='lease_payments')

    class Meta:
        verbose_name = 'Lease Payment'
        verbose_name_plural = 'Lease Payments'

    def __str__(self):
        return f'{self.tenant.first_name} {self.tenant.last_name} - {self.date}'
