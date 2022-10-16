from django.db import models
from django.db.models import Count, Max, F


class VisitorManager(models.Manager):
    def with_country_visits(self):
        return super().get_queryset()\
            .prefetch_related('towns')\
            .filter(towns__isnull=False)\
            .annotate(countries_visited=Count(F('towns__country'), distinct=True))

    def with_city_visits(self, **kwargs):
        return self.prefetch_related('towns')\
            .filter(towns__isnull=False, **kwargs)\
            .annotate(visited_cities=Count(F('towns')))

    def with_badges(self):
        return self.prefetch_related('badges')\
            .filter(badges__isnull=False)\
            .annotate(awards=Count(F('badges')))

    def get_leader_by_country(self):
        # Can be multiple users
        most_countries = self.with_country_visits().aggregate(Max('countries_visited'))['countries_visited__max']
        return self.with_country_visits().filter(countries_visited=most_countries).first()

    def get_leader_by_city(self):
        # Can be multiple users
        most_cities = self.with_city_visits().aggregate(Max('visited_cities'))['visited_cities__max']
        return self.with_city_visits().filter(visited_cities=most_cities).first()

    def get_leader_by_capital(self):
        most_capitals = self.with_city_visits(towns__capital='primary').aggregate(Max('visited_cities'))['visited_cities__max']
        return self.with_city_visits().filter(visited_cities=most_capitals).first()

    def get_leader_of_leaders(self):
        most_badges = self.with_badges().aggregate(Max('awards'))['awards__max']
        return self.with_badges().filter(awards=most_badges).first()


