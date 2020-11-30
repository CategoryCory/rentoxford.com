from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import time
import random
import math

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

    def save(self, *args, **kwargs):
        # Check if this is a new save
        is_adding = self._state.adding

        # Save new charge
        super(Charge, self).save(*args, **kwargs)

        # Find payments with remaining balance and adjust ONLY IF this is a new charge
        if is_adding is True:
            user_payments = Payment.objects.filter(tenant=self.tenant, balance__gt=0).order_by('date')
            for pmt in user_payments:
                # If charge balance is 0, no need to continue
                if self.balance <= 0:
                    break

                # Check if payment balance is greater than charge balance
                if pmt.balance >= self.balance:
                    # Payment balance is greater than charge; charge is fully paid
                    pmt.balance -= self.balance
                    self.balance = 0
                    self.status = self.PAID
                else:
                    # Payment balance is less than charge; payment balance is zero but charge still has balance
                    self.balance -= pmt.balance
                    pmt.balance = 0

                pmt.charges.add(self)
                pmt.save()

            super(Charge, self).save(*args, **kwargs)


class Payment(models.Model):
    ONLINE = 'online'
    OFFLINE = 'offline'

    TYPE_CHOICES = (
        (ONLINE, 'Online'),
        (OFFLINE, 'Offline'),
    )

    tenant = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=ONLINE)
    stripe_payment_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    confirmation = models.CharField(max_length=50, unique=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    charges = models.ManyToManyField(Charge, related_name='lease_payments', blank=True)

    class Meta:
        verbose_name = 'Lease Payment'
        verbose_name_plural = 'Lease Payments'
        indexes = [
            models.Index(fields=['confirmation'], name='confirmation_indx'),
        ]

    def __str__(self):
        return f'{self.tenant} - {self.date}'

    def save(self, *args, **kwargs):
        # Check if this is a new payment
        is_adding = self._state.adding

        # If this is a new offline payment, create a confirmation
        if is_adding and self.type == self.OFFLINE:
            char_choices = '0123456789ABCDEF'
            random_string = ''.join(random.choice(char_choices) for _ in range(16))
            self.confirmation = f'{math.floor(time.time())}-{random_string}'

        # Save new payment
        super(Payment, self).save(*args, **kwargs)

        # Find charges with remaining balance and adjust ONLY IF this is a new payment
        if is_adding is True:
            user_charges = Charge.objects.filter(tenant=self.tenant, balance__gt=0).order_by('due_date')
            for chrg in user_charges:
                # If payment balance is zero, no need to continue
                if self.balance <= 0:
                    break

                # Check if charge balance is GTE to payment balance
                if self.balance >= chrg.balance:
                    # Payment balance is GTE charge balance, payment still has balance but charge is paid
                    self.balance -= chrg.balance
                    chrg.balance = 0
                    chrg.status = Charge.PAID
                else:
                    # Payment balance is less than charge; payment is consumed
                    chrg.balance -= self.balance
                    self.balance = 0

                self.charges.add(chrg)
                chrg.save()

            super(Payment, self).save(*args, **kwargs)
