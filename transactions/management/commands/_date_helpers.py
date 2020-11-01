import datetime
from calendar import monthrange
from decimal import *


def find_next_first(curr_date):
    if curr_date.month < 12:
        return datetime.date(curr_date.year, curr_date.month+1, 1)
    else:
        return datetime.date(curr_date.year+1, 1, 1)


def find_prorated_amount(curr_year, curr_month, end_day, full_amount):
    num_days_in_month = monthrange(curr_year, curr_month)[1]
    full_amount_dec = Decimal(full_amount)
    prorate_percent = Decimal(end_day / num_days_in_month)
    return round(full_amount_dec * prorate_percent, 2)
