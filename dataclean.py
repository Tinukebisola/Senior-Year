import pandas as pd
from tabulate import tabulate
from django.conf import settings
import Realestate.settings as app_settings
from realestateapp.models import Apartment
import django
settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS, DATABASES=app_settings.DATABASES)
django.setup()


def add_all_states():
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    texas = pd.read_csv('Texas.csv')
    colorado = pd.read_csv('Colorado.csv')
    florida = pd.read_csv('Florida.csv')
    newyork = pd.read_csv('NewYork.csv')
    ohio = pd.read_csv('Ohio.csv')
    total = pd.concat([texas, colorado, florida, newyork, ohio], axis=0, ignore_index=True)
    print(tabulate(total, headers=total.columns))
    total.to_csv('Total1.csv', index=False)


def create_records(row):
    apart = Apartment.objects.create(
        min_price=float(row['min_price']),
        max_price=float(row['max_price']),
        cats = bool(row['cats']),
        dogs = bool(row['dogs']),
        pet_policy_text = row['pet_policy_text'],
        min_beds = float(row['min_beds']),
        max_beds = float(row['max_beds']),
        min_baths = float(row['min_baths']),
        max_baths = float(row['max_baths']),
        house_type = row['house_type'],
        year_built = int(row['year_built']),
        address = row['address'],
        postal_code = int(row['postal_code']),
        state = row['state'],
        city = row['city'],
        county = row['county'],
        pictures = row['pictures'],
        pictures1 = row['pictures1'],
    )
    return apart

df = pd.read_csv('Total.csv')
print(len(df))
df.dropna(axis=0, subset=['year_built'], inplace=True)
df.drop(['beds', 'price', 'baths', 'sqft'], inplace=True, axis=1)
print(len(df))
print(tabulate(df.head(5), headers=df.columns))
df['db'] = df.apply(lambda row: create_records(row), axis=1)
df.to_csv('Total.csv', index=False)

print(Apartment.objects.all())

