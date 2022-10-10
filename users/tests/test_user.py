from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.tests.factories import UserFactory


class BaseUserData(APITestCase):
    def setUp(self) -> None:
        self.users = UserFactory.create_batch(3)
        self.first_user = self.users[0]
        self.auth_client = self.client_class()
        self.auth_client.force_login(self.first_user)


class TestProfileRoute(BaseUserData):
    def test_unauthenticated_access_cannot_retrieve_user(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

    def test_can_retrieve_user_details_requested(self):
        response = self.auth_client.get(reverse('profile'))

        returned_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(returned_data.get('id'), self.first_user.id)
        for key in [
            'towns', 'badges', 'groups_owned', 'groups_requested', 'groups_joined', 'groups_podium1',
            'groups_podium2', 'groups_podium3'
        ]:
            self.assertIsNotNone(returned_data.get(key))

    def test_unauthenticated_access_cannot_update_user(self):
        response = self.client.put(reverse('profile'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

    # TODO: change to allow single field update
    def test_can_update_user_details(self):
        data = {
            **self.first_user.__dict__,
            'last_name': 'super-cool'
        }

        response = self.auth_client.put(reverse('profile'), data=data)

        returned_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(returned_data.get('last_name'), 'super-cool')
        
    def test_unauthenticated_access_cannot_delete_user(self):
        response = self.client.delete(reverse('profile'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

    def test_can_delete_user_details(self):
        response = self.auth_client.delete(reverse('profile'))

        # accepted may be a better error code here
        self.assertEqual(response.status_code, 204)
