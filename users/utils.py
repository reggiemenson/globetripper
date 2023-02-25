from dataclasses import dataclass
from typing import Union, List

from django.db.models import QuerySet, Value, FloatField
from django.db.models.functions import Cast, Replace

from users.models import User


@dataclass
class UserTravel:
    towns: Union[QuerySet, List[User.towns.model]]

    @property
    def countries(self):
        return self.towns.values_list('country', flat=True).distinct()

    @property
    def continents(self):
        return self.towns.values_list('continent', flat=True).distinct()

    @property
    def score(self):
        points = {
            'visits': self.towns.count() * 5,
            'capital_visits': self.towns.filter(capital='Primary').count() * 10,
            'country_visits': self.countries.count() * 20,
            'continent_visits': self.continents.count() * 50
        }
        return sum([total for total in points.values()])

    @property
    def is_viking(self):
        return self.towns.filter(country='United Kingdom').exists() \
               and self.towns.filter(country__in=['Denmark', 'Finland', 'Iceland', 'Norway', 'Sweden']).exists()

    @property
    def follows_columbus(self):
        return self.towns.filter(country='Spain').exists() and self.towns.filter(country='Portugal').exists() \
               and self.towns.filter(continent='South America').exists()

    @property
    def kerouac_inspired(self):
        return self.towns.filter(country='United States').count() >= 6

    @property
    def stan(self):
        return self.towns.filter(country__endswith='stan').exists()

    @property
    def towns_with_coordinates(self):
        return self.towns.annotate(
            real_latitude=Cast(Replace('latitude', Value(','), Value('.')), output_field=FloatField()))

    @property
    def reached_north_reaches(self):
        return self.towns_with_coordinates.filter(real_latitude__gte=66).exists()

    @property
    def includes_equatorial_region(self):
        return self.towns_with_coordinates.filter(real_latitude__gte=-1, real_latitude__lte=1).exists()

