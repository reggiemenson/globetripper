import factory
import faker

from travels.constants import REGISTERED_COUNTRIES
from travels.models import Town, Badge


class TownFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Town

    name = factory.Faker('city')
    # maybe change name
    name_ascii = factory.Faker('city')
    # change to latitude
    lat = factory.Faker('latitude')
    # change to longitude
    lng = factory.Faker('longitude')
    country = factory.Sequence(lambda x: REGISTERED_COUNTRIES[x % len(REGISTERED_COUNTRIES)])
    iso2 = factory.Faker('country_code')
    iso3 = factory.Faker('country_code')
    admin_name = factory.Faker('administrative_unit')
    capital = factory.Faker('city')
    population = factory.Faker('random_int')
    continent = factory.Faker('country')


class BadgeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Badge

    name = factory.Faker('name')
    description = factory.Faker('text')
    image = factory.Faker('url')


