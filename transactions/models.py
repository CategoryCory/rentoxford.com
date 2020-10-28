from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Charge(models.Model):
    DUE = 'due'
    PAID = 'paid'
    LATE = 'late'
    RENT = 'rent'
    LATE_1 = 'late_1'
    LATE_2 = 'late_2'

    STATUS_CHOICES = (
        (DUE, 'Due'),
        (PAID, 'Paid'),
        (LATE, 'Late'),
    )

    TYPE_CHOICES = (
        (RENT, 'Rent'),
        (LATE_1, 'First Late Fee'),
        (LATE_2, 'Second Late Fee'),
    )

    tenant = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    due_date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    type = models.CharField(max_length=25, choices=TYPE_CHOICES, default=RENT)
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
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    stripe_payment_id = models.CharField(max_length=50)
    notes = models.CharField(max_length=255, blank=True)
    charges = models.ManyToManyField(Charge, related_name='lease_payments')

    class Meta:
        verbose_name = 'Lease Payment'
        verbose_name_plural = 'Lease Payments'

    def __str__(self):
        return f'{self.tenant} - {self.date}'
