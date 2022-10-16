from dataclasses import dataclass
from typing import List, Union

from django.db.models import QuerySet, Value, FloatField
from django.db.models.functions import Replace, Cast

from users.models import User
from travels.models import Badge, Town, BadgeConditionGroup


def recalculate_platform_badges():
    def assign_badge(badge_id, user, criteria):
        award = Badge.objects.get(id=badge_id)
        if user and (not award.users.last() or getattr(user, criteria) > getattr(award.users.last(), criteria)):
            award.users.clear()
            award.users.add(user)

    special_scenarios = {
        (214, User.travellers.get_leader_by_country(), 'countries_visited'),
        (215, User.travellers.get_leader_by_city(), 'visited_cities'),
        (216, User.travellers.get_leader_by_capital(), 'visited_cities'),
        (217, User.travellers.get_leader_of_leaders(), 'awards')
    }

    for detail in special_scenarios:
        assign_badge(detail[0], detail[1], detail[2])


@dataclass
class UserVisits:
    towns: Union[QuerySet, List[Town]]

    @property
    def country_badges(self):
        return Badge.objects.filter(name__in=self.towns.values_list('country', flat=True).distinct())

    @property
    def continent_badges(self):
        return Badge.objects.filter(name__in=self.towns.values_list('continent', flat=True).distinct())

    @property
    def score(self):
        points = {
            'visits': self.towns.count() * 5,
            'capital_visits': self.towns.filter(capital='Primary').count() * 10,
            'country_visits': self.towns.distinct('country').count() * 20,
            'continent_visits': self.towns.distinct('continent').count() * 50
         }
        return sum([total for total in points.values()])

    @property
    def country_count_badges(self):
        try:
            condition = BadgeConditionGroup.objects.get(name='Countries Visited')
            visits = self.country_badges.count()
            badges = condition.badges.all() if visits > 5 else condition.badges.none()
            if 5 < visits < 100:
                index = (visits // 10) + 1 if visits > 10 else 1
                badges = condition.badges.all()[:index]
            return badges
        except BadgeConditionGroup.DoesNotExist:
            return Badge.objects.none()

    @property
    def city_count_badges(self):
        try:
            condition = BadgeConditionGroup.objects.get(name='Cities Visited')
            targets = [5, 10, 50, 100, 150, 200, 500]
            city_count = self.towns.count()
            badges = condition.badges.all() if city_count > targets[0] else condition.badges.none()
            if targets[0] <= city_count < targets[-1]:
                index = 1
                for i, target in enumerate(targets):
                    if city_count >= target:
                        continue
                    else:
                        index += i
                        break
                badges = condition.badges.all()[:index]
            return badges
        except BadgeConditionGroup.DoesNotExist:
            return Badge.objects.none()

    @property
    def special_condition_badges(self):
        kwargs = {
            'id__in': []
        }
        if self.is_viking:
            kwargs['id__in'].append(208)
        if self.follows_columbus:
            kwargs['id__in'].append(209)
        if self.kerouac_inspired:
            kwargs['id__in'].append(210)
        if self.stan:
            kwargs['id__in'].append(211)
        if self.reached_north_reaches:
            kwargs['id__in'].append(212)
        if self.includes_equatorial_region:
            kwargs['id__in'].append(213)

        return Badge.objects.filter(**kwargs)

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
        return self.towns.annotate(real_latitude=Cast(Replace('latitude', Value(','), Value('.')), output_field=FloatField()))

    @property
    def reached_north_reaches(self):
        return self.towns_with_coordinates.filter(real_latitude__gte=66).exists()

    @property
    def includes_equatorial_region(self):
        return self.towns_with_coordinates.filter(real_latitude__gte=-1, real_latitude__lte=1).exists()

    def get_awarded_badges(self):
        return [
            *self.country_badges, *self.country_count_badges, *self.continent_badges,
            *self.city_count_badges, *self.special_condition_badges]

