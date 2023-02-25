from travels.tests.factories import TownFactory
from travels.tests.test_badge_filtering import SetBadgeData
from users.tests.factories import UserFactory


class TestAddingTowns(SetBadgeData):

    def setUp(self) -> None:
        super().setUp()
        self.test_user = UserFactory()

    def test_adding_towns_adds_badges(self):
        uk_towns = TownFactory.create_batch(3, country='United Kingdom', continent='Europe', capital='Not Primary', latitude=5, longitude=5)
        self.test_user.add_visits(*uk_towns)

        self.assertEqual(self.test_user.badges.count(), 2)
        self.assertEqual(self.test_user.score, 85)
