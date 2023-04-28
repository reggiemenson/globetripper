from travels.constants import MOST_CAPITALS_VISITED_ID, MOST_CITIES_VISITED_ID, MOST_COUNTRIES_VISITED_ID, \
    MOST_AWARDS_ID
from travels.models import Badge
from travels.tests.factories import BadgeFactory, TownFactory
from travels.tests.test_badge_filtering import SetBadgeData
from travels.utils import recalculate_platform_badges
from users.tests.factories import UserFactory


class TestPlatformBadges(SetBadgeData):
    def setUp(self) -> None:
        super().setUp()
        self.users = UserFactory.create_batch(3)
        self.first_user = self.users[0]

    def test_user_awarded_for_most_countries(self):
        first_set = TownFactory.create_batch(2, country="United Kingdom")
        second_set = TownFactory.create_batch(2, country="France")
        third_set = TownFactory.create_batch(2, country="Spain")
        second_user = self.users[1]

        self.first_user.towns.add(*first_set, *second_set)  # more cities
        second_user.towns.add(
            first_set[0], second_set[0], third_set[0]
        )  # more countries
        self.first_user.save()
        second_user.save()

        recalculate_platform_badges()

        most_countries_badge = Badge.objects.get(id=MOST_COUNTRIES_VISITED_ID)
        self.assertEqual(most_countries_badge.users.get().id, second_user.id)

    def test_user_awarded_for_most_cities(self):
        towns = TownFactory.create_batch(8, country="United Kingdom")
        second_user = self.users[1]

        self.first_user.towns.add(*towns[2:])
        second_user.towns.add(*towns[:2])
        self.first_user.save()
        second_user.save()

        recalculate_platform_badges()

        most_cities_badge = Badge.objects.get(id=MOST_CITIES_VISITED_ID)
        self.assertEqual(most_cities_badge.users.get().id, self.first_user.id)

    def test_user_has_most_capitals(self):
        towns = TownFactory.create_batch(3, capital="primary")
        second_user = self.users[1]

        self.first_user.towns.add(towns[0])
        second_user.towns.add(*towns[1:])
        self.first_user.save()
        second_user.save()

        recalculate_platform_badges()

        most_capitals_badge = Badge.objects.get(id=MOST_CAPITALS_VISITED_ID)
        self.assertEqual(most_capitals_badge.users.get().id, second_user.id)

    def test_user_has_most_badges(self):
        """'
        Should a user only get the platform badges if they've added towns? or should they
        also be assigned if the badges are directly assigned?

        it's clear that we want the action of adding towns to be linked to the action of receiving badges.
        if the two are separate, then we have gaps in the process. adding towns should assign a score and badges

        So in this case, should badges be assigned or should towns be added?

        Well we are directly correlating badges with platform badges. This means that the input we want is
        badges and the output we want is a platform badge. If we attribute adding towns to collecting platform badges,
        a change in the way in which badges are assigned will have an unintended side effect on this unit test.
        """
        # failing test shows logic done in the view and can be circumvented. Do we want this?
        # Therefore:
        second_user = self.users[1]
        few_badges = Badge.objects.filter(id__in=[i for i in range(3)])
        more_badges = Badge.objects.filter(id__in=[n for n in range(3, 12)])

        self.first_user.badges.add(*few_badges)
        second_user.badges.add(*more_badges)
        self.first_user.save()
        second_user.save()

        recalculate_platform_badges()

        mega_badge = Badge.objects.get(id=MOST_AWARDS_ID)
        self.assertEqual(mega_badge.users.get().id, second_user.id)

    def test_first_user_receives_mega_title_if_drawn(self):
        second_user = self.users[1]
        same_badges = Badge.objects.filter(id__in=[i for i in range(5)])

        self.first_user.badges.add(*same_badges)
        second_user.badges.add(*same_badges)

        recalculate_platform_badges()

        mega_badge = Badge.objects.get(id=MOST_AWARDS_ID)
        self.assertEqual(mega_badge.users.get().id, self.first_user.id)
