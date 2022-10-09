from django.urls import reverse, reverse_lazy
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from jwt_auth.tests.factories import UserFactory


class AuthTestData(APITestCase):
    route_name = 'register'

    def setUp(self) -> None:
        self.first_user = UserFactory()
        self.password = 'amazingpassword1'
        self.first_user.set_password(self.password)
        self.first_user.save()

    def test_GET_method_is_not_allowed_on(self):

        response = self.client.get(reverse_lazy(self.route_name))

        self.assertEqual(response.status_code, 405)


class TestRegisterView(AuthTestData):
    route_name = 'register'

    def test_successful_registration_message_response_code(self):

        data = {
            'username': 'topgent',
            'first_name': 'top',
            'last_name': 'gent',
            'email': 'recognisable@gmail.com',
            'password': 'seriouspassword',
            'password_confirmation': 'seriouspassword'
        }

        response = self.client.post(reverse(self.route_name), data=data)

        self.assertEqual(response.data.get('detail'), 'Registration successful')
        self.assertEqual(response.status_code, 200)

    def test_informs_user_of_missing_info_if_not_sent(self):

        response = self.client.post(reverse(self.route_name))

        error_dict = {
            'username': [ErrorDetail(string='This field is required.', code='required')],
            'first_name': [ErrorDetail(string='This field is required.', code='required')],
            'last_name': [ErrorDetail(string='This field is required.', code='required')],
            'email': [ErrorDetail(string='This field is required.', code='required')],
            'password': [ErrorDetail(string='This field is required.', code='required')],
            'password_confirmation': [ErrorDetail(string='This field is required.', code='required')]
        }

        self.assertEqual(response.data.get('detail'), error_dict)
        self.assertEqual(response.status_code, 422)


class TestLogin(AuthTestData):
    route_name = 'login'

    def test_successful_login_attempt(self):
        login_email = self.first_user.email

        data = {
            'email': login_email,
            'password': self.password
        }

        response = self.client.post(reverse(self.route_name), data=data)

        print(response.data, 'data')
        assert False
        self.assertIsNotNone(response.data.get('token'))
        self.assertEqual(response.status_code, 200)

    def test_unknown_email_on_login_attempt(self):

        data = {
            'email': 'random@email.com',
            'password': self.password
        }

        response = self.client.post(reverse(self.route_name), data=data)

        self.assertEqual(response.data.get('detail'), 'Incorrect authentication credentials.')
        self.assertIsNone(response.data.get('token'))
        self.assertEqual(response.status_code, 401)

    def test_incorrect_password_on_login_attempt(self):
        login_email = self.first_user.email

        data = {
            'email': login_email,
            'password': 'incorrectpassword'
        }

        response = self.client.post(reverse(self.route_name), data=data)

        self.assertEqual(response.data.get('detail'), 'Incorrect authentication credentials.')
        self.assertIsNone(response.data.get('token'))
        self.assertEqual(response.status_code, 401)
