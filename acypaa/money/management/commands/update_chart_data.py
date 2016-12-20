import csv
from datetime import datetime
import os
from pytz import reference
import requests
from tzlocal import get_localzone

from django.core.management.base import BaseCommand, CommandError

from money.models import (
    Projected,
    Actual,
)

import money as money_constants

exit = os._exit

data_map = dict(
    DATE=0,
    CATEGORY=1,
    AMOUNT=2,
    DESCRIPTION=3,
    TAGS=4,
)

class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        self.tz = get_localzone()

    def handle_error(self, message, data, error):
        print message
        print 'data: %s' % data
        print 'error: %s' % error

    def format_date(self, date_string):
        try:
            if date_string[:1] == '\n':
                date_string = date_string[1:]
            if not date_string:
                return None
            if not date_string[0].isdigit():
                return None
            if date_string.find('/') < 0:
                return None
            dates = date_string.split('/')
            if int(dates[0]) < 5:
                year = 2017
            else:
                year = 2016
            month = int(dates[0])
            day = int(dates[1])
            return self.tz.localize(datetime(year, month, day))
        except Exception, e:
            self.handle_error('couldnt parse date', date_string, e)
            return None

    def format_amount(self, amount_string):
        try:
            amount = float(amount_string)
            return amount
        except Exception, e:
            self.handle_error('couldnt parse amount', amount_string, e)
            return None

    def make_dict(self, data_list):
        transaction = {}

        transaction_date = self.format_date(data_list[data_map['DATE']])
        if not transaction_date:
            return None
        transaction['date'] = transaction_date

        transaction_amount = self.format_amount(data_list[data_map['AMOUNT']])
        if not transaction_amount:
            return None
        transaction['amount'] = transaction_amount

        transaction['category'] = data_list[data_map['CATEGORY']]
        transaction['description'] = data_list[data_map['DESCRIPTION']]
        transaction['tags'] = []

        return transaction

    def get_category(self, category_string):
        transaction_category = money_constants.CATEGORY_TO_INT.get(category_string)
        if transaction_category == 'merchandise':
            transaction_category = 'merch'
        if not transaction_category:
            transaction_category = money_constants.CATEGORY_TO_INT.get('other')
            print category_string
        return transaction_category

    def fill_db(self, url, model):
        model.objects.all().delete()

        r = requests.get(url)

        for line in r.text.split('\r'):
            bits = line.split(',')
            income = bits[0:5]
            expense = bits[5:10]
            income_dict = self.make_dict(income)
            expense_dict = self.make_dict(expense)
            if income_dict:
                model.objects.create(
                    date=income_dict['date'],
                    category=self.get_category(income_dict['category']),
                    amount=income_dict['amount'],
                    description=income_dict['description'],
                    tags=income_dict['tags'],
                )
            if expense_dict:
                model.objects.create(
                    date=expense_dict['date'],
                    category=self.get_category(expense_dict['category']),
                    amount=(-1 * expense_dict['amount']),
                    description=expense_dict['description'],
                    tags=expense_dict['tags'],
                )

    def get_url(self, google_id):
        return 'https://docs.google.com/spreadsheets/d/{id}{ext}{id}'.format(
            id=google_id,
            ext='/export?format=csv&id='
        )

    def handle(self, *args, **kwargs):
        actual_url = self.get_url(money_constants.ACTUAL_GOOGLE_ID)
        projected_url = self.get_url(money_constants.PROJECTED_GOOGLE_ID)

        self.fill_db(actual_url, Actual)
        self.fill_db(projected_url, Projected)
