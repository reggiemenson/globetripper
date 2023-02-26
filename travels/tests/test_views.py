from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from travels.tests.factories import TownFactory, BadgeFactory
from users.tests.factories import UserFactory


class BaseTownData(APITestCase):
    def setUp(self) -> None:
        self.users = UserFactory.create_batch(3)
        self.first_user = self.users[0]
        self.auth_client = self.client_class()
        self.auth_client.force_login(self.first_user)
        self.uk_towns = TownFactory.create_batch(
            3,
            country="United Kingdom",
            continent="Europe",
            capital="Not Primary",
            latitude=5,
            longitude=5,
        )
        self.random_badges = BadgeFactory.create_batch(5)


class TestTownsRoute(BaseTownData):

    def test_unauthenticated_user_can_get_towns_from_get_route(self):
        created_town_ids = set(town.id for town in self.uk_towns)

        response = self.client.get(reverse("towns-v1-list"))
        returned_data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(res['id'] for res in returned_data.get("results")), created_town_ids)

    def test_other_methods_not_allowed(self):
        other_methods = ("post", "put", "patch", "delete")
        for method in other_methods:
            with self.subTest(f"making a {method} request"):
                response = getattr(self.client, method)(reverse("towns-v1-list"))
                self.assertEqual(response.status_code, 405)


class TestBadgesRoute(BaseTownData):

    def test_unauthenticated_user_cannot_get_badges_from_get_route(self):
        response = self.client.get(reverse("badges-v1-list"))
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_gets_all_badges_from_get_route(self):
        created_badge_ids = set(badge.id for badge in self.random_badges)

        response = self.auth_client.get(reverse("badges-v1-list"))
        returned_data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(res['id'] for res in returned_data.get("results")), created_badge_ids)

    def test_retrieve_single_badge_from_get_route(self):
        query_id = self.random_badges[0].id

        response = self.auth_client.get(reverse("badges-v1-detail", kwargs={'pk': query_id}))
        returned_data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(returned_data.get("id"), query_id)

    def test_other_methods_not_allowed(self):
        other_methods = ("post", "put", "patch", "delete")
        for method in other_methods:
            with self.subTest(f"making a {method} request"):
                response = getattr(self.auth_client, method)(reverse("badges-v1-list"))
                self.assertEqual(response.status_code, 405)
