from decimal import Decimal

from rest_framework.test import APITestCase

from travels.constants import CONTINENTS, REGISTERED_COUNTRIES
from travels.models import Badge
from travels.tests.factories import BadgeFactory, TownFactory, BadgeConditionGroupFactory
from travels.utils import recalculate_platform_badges, UserVisits
from users.tests.factories import UserFactory


class SetBadgeData(APITestCase):
    def setUp(self) -> None:
        self.country_visit_condition = BadgeConditionGroupFactory(name='Countries Visited')
        self.city_visit_condition = BadgeConditionGroupFactory(name='Cities Visited')
        for i, name in enumerate(REGISTERED_COUNTRIES):
            country_id = 1 + i
            BadgeFactory(id=country_id, name=name)

        for n in range(184, 202):
            if n < 195:
                BadgeFactory(id=n, condition=self.country_visit_condition)
            else:
                BadgeFactory(id=n, condition=self.city_visit_condition)

        for i, name in enumerate(CONTINENTS[:6]):
            continent_id = 202 + i
            BadgeFactory(id=continent_id, name=name)

        for n in range(208, 218):
            BadgeFactory(id=n)

        self.users = UserFactory.create_batch(3)
        self.first_user = self.users[0]
        self.london = TownFactory(name='London', country='United Kingdom', continent='Europe', latitude='22')
        self.paris = TownFactory(name='Paris', country='France', continent='Europe', latitude='22')
        self.tokyo = TownFactory(name='Tokyo', country='Japan', continent='Asia', latitude='22')
        self.sao_paolo = TownFactory(name='Sao Paolo', country='Brazil', continent='South America', latitude='22')
        self.cape_town = TownFactory(name='Cape Town', country='South Africa', continent='Africa', latitude='22')


class TestUserBadges(SetBadgeData):

    def test_user_with_no_towns_assigns_no_badge(self):
        first_user_vists = UserVisits(self.first_user.towns)

        self.assertEqual(len(first_user_vists.get_awarded_badges()), 0)

    def testing_adding_town_adds_country_and_continent_badge(self):
        europe_id = 202
        united_kingdom_id = 175

        self.first_user.towns.add(self.london)
        self.first_user.save()

        badges = UserVisits(self.first_user.towns).get_awarded_badges()
        badge_ids = [badge.id for badge in badges]

        self.assertIn(europe_id, badge_ids)
        self.assertIn(united_kingdom_id, badge_ids)
        self.assertEqual(len(badges), 2)

    def test_adding_countries_adds_relevant_badges(self):
        # possible bug on multiple runs: Is a unique country always guaranteed with Faker?
        towns = TownFactory.create_batch(100, name='one city, many nations')
        for i in range(0, 101, 10):
            self.first_user.towns.add(*towns[i: i + 10])
            self.first_user.save()
            with self.subTest(f"adding {i + 10}"):
                country_badge_ids = self.country_visit_condition.badges.values_list('id', flat=True)
                badges = UserVisits(self.first_user.towns).get_awarded_badges()
                badge_ids = [badge.id for badge in badges]
                self.assertIn(country_badge_ids[i//10], badge_ids)

    def test_adding_cities_adds_relevant_badges(self):
        towns = TownFactory.create_batch(500)
        for num, x in enumerate([5, 10, 50, 100, 150, 200, 500]):
            with self.subTest(f"adding {x}"):
                self.first_user.towns.add(*towns[:x])
                self.first_user.save()
                city_badge_ids = self.city_visit_condition.badges.values_list('id', flat=True)
                badges = UserVisits(self.first_user.towns).get_awarded_badges()
                badge_ids = [badge.id for badge in badges]
                self.assertIn(city_badge_ids[num], badge_ids)

    def test_special_criteria_badges(self):
        # clean up these tests when refactored
        conditions = [
            'Scandinavian + UK',
            'Spain + Portugal + South America',
            '6 in America',
            "'stan' suffixed'",
            'The Arctic',
            'The Equator',
        ]
        for i in range(6):
            qualifying_towns = [
                [TownFactory(country='Norway'), TownFactory(country='United Kingdom')],
                [TownFactory(country='Spain'), TownFactory(country='Portugal'), TownFactory(continent='South America')],
                TownFactory.create_batch(6, country='United States'),
                [TownFactory(country='Afghanistan')],
                [TownFactory(latitude=Decimal('67.244262'))],
                [TownFactory(latitude=Decimal('0.244262'), longitude=Decimal('-0.244262'))]
            ][i]
            with self.subTest(f"if visited {conditions[i]}..."):
                self.first_user.towns.add(*qualifying_towns)
                self.first_user.save()
                special_badge_ids = [i for i in range(208, 214)]
                badges = UserVisits(self.first_user.towns).get_awarded_badges()
                badge_ids = [badge.id for badge in badges]
                self.assertIn(special_badge_ids[i], badge_ids)


class TestPlatformBadges(SetBadgeData):
    def test_user_awarded_for_most_countries(self):
        first_set = TownFactory.create_batch(2, country='United Kingdom')
        second_set = TownFactory.create_batch(2, country="France")
        third_set = TownFactory.create_batch(2, country="Spain")
        second_user = self.users[1]

        self.first_user.towns.add(*first_set, *second_set)  # more cities
        second_user.towns.add(first_set[0], second_set[0], third_set[0])  # more countries
        self.first_user.save()
        second_user.save()

        recalculate_platform_badges()

        most_countries_badge = Badge.objects.get(id=214)
        self.assertEqual(most_countries_badge.users.get().id, second_user.id)

    def test_user_awarded_for_most_cities(self):
        towns = TownFactory.create_batch(8, country='United Kingdom')
        second_user = self.users[1]

        self.first_user.towns.add(*towns[2:])
        second_user.towns.add(*towns[:2])
        self.first_user.save()
        second_user.save()

        recalculate_platform_badges()

        most_cities_badge = Badge.objects.get(id=215)
        self.assertEqual(most_cities_badge.users.get().id, self.first_user.id)

    def test_user_has_most_capitals(self):
        towns = TownFactory.create_batch(3, capital='primary')
        second_user = self.users[1]

        self.first_user.towns.add(towns[0])
        second_user.towns.add(*towns[1:])
        self.first_user.save()
        second_user.save()

        recalculate_platform_badges()

        most_capitals_badge = Badge.objects.get(id=216)
        self.assertEqual(most_capitals_badge.users.get().id, second_user.id)

    def test_user_has_most_badges(self):
        second_user = self.users[1]
        few_badges = Badge.objects.filter(id__in=[i for i in range(3)])
        more_badges = Badge.objects.filter(id__in=[n for n in range(3, 12)])

        self.first_user.badges.add(*few_badges)
        second_user.badges.add(*more_badges)
        self.first_user.save()
        second_user.save()

        recalculate_platform_badges()

        mega_badge = Badge.objects.get(id=217)
        self.assertEqual(mega_badge.users.get().id, second_user.id)

    def test_first_user_receives_mega_title_if_drawn(self):
        second_user = self.users[1]
        same_badges = Badge.objects.filter(id__in=[i for i in range(5)])

        self.first_user.badges.add(*same_badges)
        second_user.badges.add(*same_badges)
        self.first_user.save()
        second_user.save()

        recalculate_platform_badges()

        mega_badge = Badge.objects.get(id=217)
        self.assertEqual(mega_badge.users.get().id, self.first_user.id)
