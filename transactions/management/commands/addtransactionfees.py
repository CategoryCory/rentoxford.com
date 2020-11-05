from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from datetime import date
from transactions.models import Charge
from ._date_helpers import find_current_first, find_next_first, find_prorated_amount
from decimal import Decimal
import math

CustomUser = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        charges = Charge.objects.filter(balance__gt=0)
        for chrg in charges:
            # Get transaction fee as cents and round down
            transaction_fee = ((chrg.amount + Decimal(0.3)) / Decimal(0.971)) - chrg.amount
            transaction_fee = round(transaction_fee, 2)

            # Add transaction fee to balance, if balance is still full
            if chrg.balance == chrg.amount:
                chrg.balance += transaction_fee

            # Add transaction fee to amount
            chrg.amount += transaction_fee

            # Save modified charge
            chrg.save()
