from django.db import models
from django.db.models import Count, Max, F

from travels.constants import MOST_AWARDS_ID


class VisitorManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("towns")
            .filter(towns__isnull=False)
            .prefetch_related("badges")
            .annotate(
                countries_visited=Count(F("towns__country"), distinct=True),
                visited_cities=Count(F("towns")),
                awards=Count(F("badges")),
            )
        )

    def get_leader_by_country(self):
        return self.get_queryset().order_by("-countries_visited").first()

    def get_leader_by_city(self):
        return self.get_queryset().order_by("-visited_cities").first()

    def get_leader_by_capital(self):
        return (
            self.get_queryset()
            .filter(towns__capital="primary")
            .order_by("-visited_cities")
            .first()
        )


class CustomUserManager(models.Manager):
    def with_badges(self):
        return (
            self.prefetch_related("badges")
            .filter(badges__isnull=False)
            .annotate(awards=Count(F("badges")))
        )

    def get_leader_of_leaders(self):
        return self.with_badges().exclude(id=MOST_AWARDS_ID).order_by("-awards", "date_joined").first()
