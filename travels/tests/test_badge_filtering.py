from decimal import Decimal

from rest_framework.test import APITestCase

from travels.constants import CONTINENTS, REGISTERED_COUNTRIES, CITY_VISIT_BADGES
from travels.models import Badge, Town
from travels.tests.factories import BadgeFactory, TownFactory


class SetBadgeData(APITestCase):
    def setUp(self) -> None:
        for i, name in enumerate(REGISTERED_COUNTRIES):
            country_id = 1 + i
            BadgeFactory(id=country_id, name=name)

        for n in range(184, 202):
            if n < 195:
                BadgeFactory(id=n)
            else:
                BadgeFactory(id=n)

        for i, name in enumerate(CONTINENTS[:6]):
            continent_id = 202 + i
            BadgeFactory(id=continent_id, name=name)

        for n in range(208, 218):
            BadgeFactory(id=n)

        self.london = TownFactory(
            name="London", country="United Kingdom", continent="Europe", latitude="22"
        )
        self.paris = TownFactory(
            name="Paris", country="France", continent="Europe", latitude="22"
        )
        self.tokyo = TownFactory(
            name="Tokyo", country="Japan", continent="Asia", latitude="22"
        )
        self.sao_paolo = TownFactory(
            name="Sao Paolo", country="Brazil", continent="South America", latitude="22"
        )
        self.cape_town = TownFactory(
            name="Cape Town", country="South Africa", continent="Africa", latitude="22"
        )


class TestBadgeFiltering(SetBadgeData):
    def test_filtering_with_no_towns_returns_no_results(self):
        qualifying_badges = Badge.objects.get_qualifying_badges(
            towns=Town.objects.none()
        )

        self.assertEqual(len(qualifying_badges), 0)

    def testing_adding_town_adds_country_and_continent_badge(self):
        europe_id = 202
        united_kingdom_id = 175

        country_and_continent_badges = Badge.objects.get_qualifying_badges(
            towns=Town.objects.filter(id=self.london.id)
        )
        badge_ids = [badge.id for badge in country_and_continent_badges]

        self.assertIn(europe_id, badge_ids)
        self.assertIn(united_kingdom_id, badge_ids)
        self.assertEqual(len(country_and_continent_badges), 2)

    def test_adding_countries_adds_matching_country_badges(self):
        # Factories generate sequential data from registered countries
        towns = TownFactory.create_batch(
            100,
            name="one city",
            continent="one continent",
            capital="Not Primary",
            latitude=25,
        )
        for i in range(0, 101, 10):
            with self.subTest(f"adding {i + 10}"):
                town_queryset = Town.objects.filter(
                    id__in=[town.id for town in towns[i : i + 10]]
                )
                badge_result = Badge.objects.get_qualifying_badges(towns=town_queryset)
                country_names = list(town_queryset.values_list("country", flat=True))
                num_of_country_badges = badge_result.filter(
                    name__in=country_names
                ).count()
                self.assertEqual(len(country_names), num_of_country_badges)

    def test_adding_cities_adds_relevant_badges(self):
        towns = TownFactory.create_batch(500)
        for num, x in enumerate([5, 10, 50, 100, 150, 200, 500]):
            with self.subTest(f"adding {x}"):
                town_queryset = Town.objects.filter(
                    id__in=[town.id for town in towns[:x]]
                )
                badge_result = Badge.objects.get_qualifying_badges(towns=town_queryset)
                badge_result.get(id=CITY_VISIT_BADGES.get(str(x)))

    def test_special_criteria_badges(self):
        # clean up these tests when refactored
        conditions = [
            "Scandinavian + UK",
            "Spain + Portugal + South America",
            "6 in America",
            "'stan' suffixed'",
            "The Arctic",
            "The Equator",
        ]
        for i in range(6):
            qualifying_towns = [
                [TownFactory(country="Norway"), TownFactory(country="United Kingdom")],
                [
                    TownFactory(country="Spain"),
                    TownFactory(country="Portugal"),
                    TownFactory(continent="South America"),
                ],
                TownFactory.create_batch(6, country="United States"),
                [TownFactory(country="Afghanistan")],
                [TownFactory(latitude=Decimal("67.244262"))],
                [
                    TownFactory(
                        latitude=Decimal("0.244262"), longitude=Decimal("-0.244262")
                    )
                ],
            ][i]
            with self.subTest(f"if visited {conditions[i]}..."):
                special_badge_ids = [i for i in range(208, 214)]
                town_queryset = Town.objects.filter(
                    id__in=[town.id for town in qualifying_towns]
                )
                badge_result = Badge.objects.get_qualifying_badges(towns=town_queryset)
                badge_ids = [badge.id for badge in badge_result]
                self.assertIn(special_badge_ids[i], badge_ids)
