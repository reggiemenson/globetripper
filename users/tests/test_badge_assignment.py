from decimal import Decimal

from rest_framework.test import APITestCase

from travels.models import Badge
from travels.tests.factories import BadgeFactory, TownFactory
from users.badge_logic import get_user_badges, get_most_countries_badge, get_most_cities_badge, get_most_badges_badge, \
    get_most_capitals_badge
from users.models import User
from users.serializers import PopulatedUserSerializer
from users.tests.factories import UserFactory


class SetBadgeData(APITestCase):
    def setUp(self) -> None:
        for i in range(1, 218):
            BadgeFactory(id=i)
        self.users = UserFactory.create_batch(3)
        self.first_user = self.users[0]
        self.london = TownFactory(name='London', country='United Kingdom', continent="Europe")
        self.paris = TownFactory(name='Paris', country='France', continent='Europe')
        self.tokyo = TownFactory(name='Tokyo', country='Japan', continent='Asia')
        self.sao_paolo = TownFactory(name='Sao Paolo', country='Brazil', continent='South America')
        self.cape_town = TownFactory(name='Cape Town', country='South Africa', continent='Africa')


class TestUserBadges(SetBadgeData):

    def test_user_with_no_towns_assigns_no_badge(self):
        populated_user = PopulatedUserSerializer(self.first_user)
        badges = get_user_badges(populated_user)

        self.assertEqual(len(badges), 0)

    def testing_adding_town_adds_country_and_continent_badge(self):
        europe_id = 202
        united_kingdom_id = 175

        self.first_user.towns.add(self.london)
        self.first_user.save()

        populated_user = PopulatedUserSerializer(self.first_user)
        badges = get_user_badges(populated_user)

        self.assertIn(europe_id, badges)
        self.assertIn(united_kingdom_id, badges)
        self.assertEqual(len(badges), 2)

    def test_adding_countries_adds_relevant_badges(self):
        # possible bug on multiple runs: Is a unique country always guaranteed with Faker?
        towns = TownFactory.create_batch(100)
        for i in range(0, 101, 10):
            self.first_user.towns.add(*towns[i: i + 10])
            self.first_user.save()
            with self.subTest(f"adding {i + 10}"):
                country_badge_ids = [n for n in range(184, 195)]
                populated_user = PopulatedUserSerializer(self.first_user)
                badges = get_user_badges(populated_user)
                self.assertIn(next(iter(country_badge_ids)), badges)

    def test_adding_cities_adds_relevant_badges(self):
        towns = TownFactory.create_batch(100)
        for i in range(0, 501, 10):
            with self.subTest(f"adding {i + 10}"):
                self.first_user.towns.add(*towns[i: i + 10])
                self.first_user.save()
                city_badge_ids = [n for n in range(195, 202)]
                populated_user = PopulatedUserSerializer(self.first_user)
                badges = get_user_badges(populated_user)
                self.assertIn(next(iter(city_badge_ids)), badges)

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
                [TownFactory(lat=Decimal('67.244262'))],
                [TownFactory(lat=Decimal('0.244262'), lng=Decimal('-0.244262'))]
            ][i]
            with self.subTest(f"if visited {conditions[i]}..."):
                self.first_user.towns.add(*qualifying_towns)
                self.first_user.save()
                city_badge_ids = [n for n in range(208, 214)]
                populated_user = PopulatedUserSerializer(self.first_user)
                badges = get_user_badges(populated_user)
                self.assertIn(city_badge_ids[i], badges)


class TestPlatformBadges(SetBadgeData):
    def test_user_awarded_for_most_countries(self):
        towns = TownFactory.create_batch(4)
        second_user = self.users[1]

        self.first_user.towns.add(towns[0])
        second_user.towns.add(*towns[1:])
        self.first_user.save()
        second_user.save()

        all_users = User.objects.all()
        serialized_users = PopulatedUserSerializer(all_users, many=True)
        get_most_countries_badge(serialized_users)

        most_countries_badge = Badge.objects.get(id=214)
        self.assertEqual(most_countries_badge.users.get().id, second_user.id)

    def test_user_awarded_for_most_cities(self):
        towns = TownFactory.create_batch(8)
        second_user = self.users[1]

        self.first_user.towns.add(*towns[2:])
        second_user.towns.add(*towns[:2])
        self.first_user.save()
        second_user.save()

        all_users = User.objects.all()
        serialized_users = PopulatedUserSerializer(all_users, many=True)
        get_most_cities_badge(serialized_users)

        most_cities_badge = Badge.objects.get(id=215)
        self.assertEqual(most_cities_badge.users.get().id, self.first_user.id)

    def test_user_has_most_capitals(self):
        towns = TownFactory.create_batch(3, capital='primary')
        second_user = self.users[1]

        self.first_user.towns.add(towns[0])
        second_user.towns.add(*towns[1:])
        self.first_user.save()
        second_user.save()

        all_users = User.objects.all()
        serialized_users = PopulatedUserSerializer(all_users, many=True)
        get_most_capitals_badge(serialized_users)

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

        all_users = User.objects.all()
        serialized_users = PopulatedUserSerializer(all_users, many=True)
        get_most_badges_badge(serialized_users)

        mega_badge = Badge.objects.get(id=217)
        self.assertEqual(mega_badge.users.get().id, second_user.id)

    def test_first_user_receives_mega_title_if_drawn(self):
        second_user = self.users[1]
        same_badges = Badge.objects.filter(id__in=[i for i in range(5)])

        self.first_user.badges.add(*same_badges)
        second_user.badges.add(*same_badges)
        self.first_user.save()
        second_user.save()

        all_users = User.objects.all()
        serialized_users = PopulatedUserSerializer(all_users, many=True)
        get_most_badges_badge(serialized_users)

        mega_badge = Badge.objects.get(id=217)
        self.assertEqual(mega_badge.users.get().id, self.first_user.id)
