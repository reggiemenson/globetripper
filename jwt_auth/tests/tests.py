from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase


class TestRegisterView(APITestCase):
    """
    Tests covering the Register route
    """

    def test_to_GET_method_is_not_allowed(self):

        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 405)

    def test_successful_registration(self):

        data = {
            'username': 'topgent',
            'first_name': 'top',
            'last_name': 'gent',
            'email': 'recognisable@gmail.com',
            'password': 'seriouspassword',
            'password_confirmation': 'seriouspassword'
        }

        response = self.client.post(reverse('register'), data=data)

        self.assertEqual(response.data.get('message'), 'Registration successful')
        self.assertEqual(response.status_code, 200)

    def test_informs_user_of_missing_info_if_not_sent(self):

        response = self.client.post(reverse('register'))

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
