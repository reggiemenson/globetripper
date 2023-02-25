from django.db import models

from dataclasses import dataclass
from typing import List, Union

from django.db.models import QuerySet, Value, FloatField, Q
from django.db.models.functions import Replace, Cast

from travels.constants import CITY_VISIT_BADGES, COUNTRY_VISIT_BADGES


class BadgeAssignmentManager(models.Manager):

    def get_qualifying_badges(self, towns):
        travels = Travel(towns)

        queries = [
                Q(name__in=list(towns.values_list('country', flat=True).distinct()) + list(towns.values_list('continent', flat=True).distinct())),
                Q(id__in=[b for count, b in COUNTRY_VISIT_BADGES.items() if
                          towns.values_list('country', flat=True).distinct().count() >= int(count)] + [b for count, b in CITY_VISIT_BADGES.items() if towns.count() >= int(count)])
        ]
        special_queries = award_special_targets(travels)

        check = self.get_queryset().all().filter(queries[0] | queries[1] | special_queries)
        return check


class TownManager(models.Manager):

    def count_travel_score(self):
        return Travel(self).score


@dataclass
class Travel:
    towns: Union[QuerySet, List['Town']]

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


def construct_badge_queries(towns):
    # evaluate = towns.values_list('country', flat=True).distinct()
    country_badges = {
        '184': 5,
        '185': 10,
        '186': 20,
        '187': 30,
        '188': 40,
        '189': 50,
        '190': 60,
        '191': 70,
        '192': 80,
        '193': 90,
        '194': 100,
    }
    city_badges = {
        '195': 5,
        '196': 10,
        '197': 50,
        '198': 100,
        '199': 150,
        '200': 200,
        '201': 500
    }
    return (
        Q(name__in=towns.values_list('country', flat=True).distinct()) |
        Q(name__in=towns.values_list('continent', flat=True).distinct()) |
        Q(id__in=[int(k) for k, count in country_badges.items() if towns.values_list('country', flat=True).distinct().count() > count]) |
        Q(id__in=[int(k) for k, count in city_badges.items() if towns.count() > count])
    )


def award_special_targets(travels):
    ids = []
    if travels.is_viking:
        ids.append(208)
    if travels.follows_columbus:
        ids.append(209)
    if travels.kerouac_inspired:
        ids.append(210)
    if travels.stan:
        ids.append(211)
    if travels.reached_north_reaches:
        ids.append(212)
    if travels.includes_equatorial_region:
        ids.append(213)
    return Q(id__in=ids)
