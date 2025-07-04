from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user_auth.models import User
# Create your tests here.


class RegisterViewTest(APITestCase):
    def test_register_view(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeated_password': 'testpassword',
            'type': 'customer'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Korrekte Methode für Dictionary-Responses:
        self.assertIn('token', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('user_id', response.data)

        # Zusätzliche Token-Validierungen:
        token = response.data['token']
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)

        data2 = {
            'username': 'testuser2',
            'email': 'testuser@example2.com',
            'password': 'testpassword',
            'repeated_password': 'testpassword',
            'type': 'business'
        }
        response2 = self.client.post(url, data2)

        # Fehlermeldung ausloggen
        if response2.status_code != status.HTTP_201_CREATED:
            print(f"Status Code: {response2.status_code}")
            print(f"Response Data: {response2.data}")
            print("-----------------------_-----------------------asasasasas")

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def test_register_view_with_invalid_data(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeated_password': 'testpassword',
            'type': 'wrong_type'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('type', response.data)


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_login_view(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('user_id', response.data)

    def test_login_view_with_invalid_credentials(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

        data2 = {
            'username': 'testuser'
        }
        response2 = self.client.post(url, data2)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response2.data)

        data3 = {
            'password': 'testpassword'
        }
        response3 = self.client.post(url, data3)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
