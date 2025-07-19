from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterViewTests(APITestCase):
    def test_register_user_success(self):
        url = reverse('register')
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_user_missing_password(self):
        url = reverse('register')
        data = {
            "username": "testuser",
            "email": "test@example.com",
            # password missing
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="oldpassword")
        self.client.force_authenticate(user=self.user)
        self.url = reverse('user_profile')

    def test_update_name_success(self):
        data = {
            "first_name": "NewFirst",
            "last_name": "NewLast"
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "NewFirst")
        self.assertEqual(self.user.last_name, "NewLast")

    def test_update_password_wrong_old_password(self):
        data = {
            "old_password": "wrongpassword",
            "new_password": "newstrongpassword"
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_update_password_success(self):
        data = {
            "old_password": "oldpassword",
            "new_password": "newstrongpassword"
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newstrongpassword"))
