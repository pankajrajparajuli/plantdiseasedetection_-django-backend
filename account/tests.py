from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountTests(APITestCase):
    def setUp(self):
        # Create a test user for authentication tests
        self.user = User.objects.create_user(
            username='testuser',
            email="testuser@example.com",
            password="securepassword123",
            first_name="Test",
            last_name="User"
        )
        # URL endpoints, names must match your urls.py
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.register_url = reverse('register')
        self.logout_url = reverse('logout')
        self.user_detail_url = reverse('user_detail')  # from your urls.py
        self.user_update_url = reverse('user_profile')  # from your urls.py

    def authenticate(self):
        # Helper to login and set auth header with username (not email)
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_register_user(self):
        # Test successful registration requires username too!
        response = self.client.post(self.register_url, {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass1234",
            "first_name": "New",
            "last_name": "User"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_logout_user(self):
        # Test logout (blacklist refresh token)
        self.authenticate()
        response = self.client.post(self.logout_url, {"refresh": self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_user_detail_view(self):
        # Test retrieving user details
        self.authenticate()
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], "testuser@example.com")

    def test_update_user_profile_without_password(self):
        # Test updating first and last name only
        self.authenticate()
        response = self.client.put(self.user_update_url, {
            "first_name": "Updated",
            "last_name": "Name"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "Name")

    def test_update_password_with_old_password(self):
        # Test updating password with correct old password
        self.authenticate()
        response = self.client.put(self.user_update_url, {
            "old_password": "securepassword123",
            "new_password": "newsecurepassword456"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newsecurepassword456"))

    def test_update_password_without_old_password(self):
        # Test updating password without old password (should fail)
        self.authenticate()
        response = self.client.put(self.user_update_url, {
            "new_password": "newsecurepassword456"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_update_password_with_wrong_old_password(self):
        # Test updating password with wrong old password (should fail)
        self.authenticate()
        response = self.client.put(self.user_update_url, {
            "old_password": "wrongpassword",
            "new_password": "newsecurepassword456"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
