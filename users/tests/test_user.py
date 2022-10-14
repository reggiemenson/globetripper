from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from travels.tests.factories import TownFactory, BadgeFactory
from users.models import User
from users.tests.factories import UserFactory


class BaseUserData(APITestCase):
    def setUp(self) -> None:
        for i in range(1, 218):
            BadgeFactory(id=i)
        self.users = UserFactory.create_batch(3)
        self.first_user = self.users[0]
        self.auth_client = self.client_class()
        self.auth_client.force_login(self.first_user)


class TestProfileRoute(BaseUserData):
    def test_unauthenticated_access_cannot_retrieve_user(self):
        response = self.client.get(reverse('profile-v1'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

    def test_can_retrieve_user_details_requested(self):
        response = self.auth_client.get(reverse('profile-v1'))

        returned_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(returned_data.get('id'), self.first_user.id)
        for key in [
            'towns', 'badges', 'groups_owned', 'groups_requested', 'groups_joined', 'groups_podium1',
            'groups_podium2', 'groups_podium3'
        ]:
            self.assertIsNotNone(returned_data.get(key))

    def test_unauthenticated_access_cannot_update_user(self):
        response = self.client.put(reverse('profile-v1'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

    # TODO: change to allow single field update
    def test_can_update_user_details(self):
        data = {
            **self.first_user.__dict__,
            'last_name': 'super-cool'
        }

        response = self.auth_client.put(reverse('profile-v1'), data=data)

        returned_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(returned_data.get('last_name'), 'super-cool')

    def test_unauthenticated_access_cannot_delete_user(self):
        response = self.client.delete(reverse('profile-v1'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

    def test_can_delete_user_details(self):
        response = self.auth_client.delete(reverse('profile-v1'))

        self.assertEqual(response.status_code, 204)


class TestGetUserRoutes(BaseUserData):
    # need tests for incorrect methods
    def test_unauthenticated_cannot_retrieve_user_by_id(self):
        response = self.client.get(reverse('users-v1-detail', [self.first_user.id]))

        self.assertEqual(response.status_code, 401)

    # Do we want this behaviour?
    def test_unauthenticated_can_retrieve_user_list(self):
        response = self.client.get(reverse('users-v1-list'))

        test_users = User.objects.all()
        test_user_list = test_users.values_list('id', flat=True)

        self.assertEqual(response.status_code, 200)
        for obj in response.data:
            self.assertIn(obj.get('id'), test_user_list)

    def test_retrieve_user_with_passed_id(self):
        response = self.auth_client.get(reverse('users-v1-detail', [self.first_user.id]))

        result = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['id'], self.first_user.id)


class TestEditUserRoutes(BaseUserData):
    # update a town with this route
    def test_unauthenticated_cannot_access_route(self):
        response = self.client.put(reverse('profile-v1-town'))

        self.assertEqual(response.status_code, 401)

    def test_update_town_successfully(self):
        mock_towns = TownFactory.create_batch(3)
        selected_town_ids = [town.id for town in mock_towns][:1]
        data = {
            'username': self.first_user.username,
            'first_name': self.first_user.first_name,
            'last_name': self.first_user.last_name,
            'towns': selected_town_ids
        }
        response = self.auth_client.put(reverse('profile-v1-town'), data)

        result = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['towns'], selected_town_ids)

    def test_update_with_incorrect_data_raises_expected_response_code(self):
        data = {
            'username': self.first_user.username,
            'first_name': self.first_user.first_name,
            'last_name': self.first_user.last_name,
            'towns': [1, 2, 3]
        }
        response = self.auth_client.put(reverse('profile-v1-town'), data)

        self.assertEqual(response.status_code, 400)
