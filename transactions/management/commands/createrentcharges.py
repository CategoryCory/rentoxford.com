from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from datetime import date
from transactions.models import Charge
from ._date_helpers import find_current_first, find_next_first, find_prorated_amount
from decimal import Decimal

CustomUser = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--currentmonth',
            action='store_true',
            help='Process rent charges for current month instead of the following month'
        )

    def handle(self, *args, **options):
        today = date.today()
        users = CustomUser.objects.filter(is_approved=True, is_staff=False)

        if options['currentmonth']:
            # If currentmonth argument is passed, process charges for the current month
            next_due_date = find_current_first(today)
        else:
            # Process charges for the following month
            next_due_date = find_next_first(today)

        second_due_date = find_next_first(next_due_date)
        for user in users:
            try:
                # Check if user has lease
                user_lease = user.lease
                if not user_lease:
                    continue
                else:
                    # User has lease; check if lease is still current
                    if user_lease.lease_end <= today:
                        continue
                    # Lease is still current; check if next charge already exists
                    next_charge = Charge.objects.filter(tenant=user, due_date=next_due_date)
                    if not next_charge:
                        # Next charge doesn't exist; create new charge
                        next_charge = Charge(
                            tenant=user,
                            due_date=next_due_date,
                            type=Charge.RENT,
                            status=Charge.DUE,
                            notes=f'Rent charge for {next_due_date}'
                        )
                        # Check if next charge should be for full month
                        if user_lease.lease_end >= second_due_date:
                            # Next charge should be for full month
                            next_charge.amount = user.rent_amount
                            next_charge.balance = user.rent_amount
                        else:
                            # Next charge should be prorated
                            prorated_amount = find_prorated_amount(
                                next_due_date.year,
                                next_due_date.month,
                                user_lease.lease_end.day,
                                user.rent_amount
                            )
                            next_charge.amount = prorated_amount
                            next_charge.balance = prorated_amount

                        # Adjust amount for transaction fee
                        transaction_fee = ((next_charge.amount + Decimal(0.3)) / Decimal(0.971)) - next_charge.amount
                        transaction_fee = round(transaction_fee, 2)
                        next_charge.amount += transaction_fee
                        next_charge.balance += transaction_fee

                        # Save new charge
                        next_charge.save()
            except Exception as e:
                print(str(e))
