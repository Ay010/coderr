from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from user_auth.models import User

# Create your tests here.


class ProfileTestCase(TestCase):

    def setUp(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeated_password': 'testpassword',
            'type': 'customer'
        }
        response = self.client.post(url, data)

        token = Token.objects.get(user__username='testuser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client = client

        data2 = {
            'username': 'businessUser',
            'email': 'businessuser@example.com',
            'password': 'testpassword',
            'repeated_password': 'testpassword',
            'type': 'business'
        }
        response2 = self.client.post(url, data2)

        data3 = {
            'username': 'customerUser',
            'email': 'customeruser@example.com',
            'password': 'testpassword',
            'repeated_password': 'testpassword',
            'type': 'customer'
        }
        response3 = self.client.post(url, data3)

    def test_profile_creation(self):
        user_id = User.objects.get(username='testuser').id

        url = reverse('profile-detail', kwargs={'pk': user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')
        self.assertEqual(response.data['type'], 'customer')
        self.assertEqual(response.data['user'], user_id)

    def test_profile_fail(self):
        url = reverse('profile-detail', kwargs={'pk': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + '1234567890')
        client = client

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_update(self):
        user_id = User.objects.get(username='testuser').id
        url = reverse('profile-detail', kwargs={'pk': user_id})
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'location': 'Berlin',
            'tel': '1234567890',
            'description': 'Test description',
            'working_hours': '9-17',
            'email': 'testuser2@example.com'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['location'], 'Berlin')
        self.assertEqual(response.data['tel'], '1234567890')
        self.assertEqual(response.data['description'], 'Test description')
        self.assertEqual(response.data['working_hours'], '9-17')
        self.assertEqual(response.data['email'], 'testuser2@example.com')

    def test_list_business_and_customer_profiles(self):
        url = reverse('list-business-profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['type'], 'business')

        url = reverse('list-customer-profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['type'], 'customer')
