from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from datetime import date
from transactions.models import Charge
from ._date_helpers import find_next_first, find_prorated_amount

CustomUser = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        today = date.today()
        next_due_date = find_next_first(today)
        second_due_date = find_next_first(next_due_date)
        users = CustomUser.objects.filter(is_approved=True, is_staff=False)
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
                        # Save new charge
                        next_charge.save()
            except Exception as e:
                print(str(e))
