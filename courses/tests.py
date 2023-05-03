from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_signup_form_valid(self):
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Your registration has been completed successfully.')
        self.assertEqual(User.objects.count(), 1)

    def test_signup_form_invalid(self):
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid request.')
        self.assertEqual(User.objects.count(), 0)
