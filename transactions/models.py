from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Charge(models.Model):
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
        return f'{self.tenant} - {self.due_date}'


class Payment(models.Model):
    tenant = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    notes = models.CharField(max_length=255, blank=True)
    charges = models.ManyToManyField(Charge, related_name='lease_payments')

    class Meta:
        verbose_name = 'Lease Payment'
        verbose_name_plural = 'Lease Payments'

    def __str__(self):
        return f'{self.tenant} - {self.date}'
