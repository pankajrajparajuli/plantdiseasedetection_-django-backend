from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()  # Use get_user_model() for custom user models compatibility


class AccountTests(APITestCase):
    def setUp(self):
        """
        setUp is called before every test method to create initial data.
        Here we create a test user and define endpoint URLs to reuse.
        Using reverse() ensures URL resolution stays consistent with urls.py.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email="testuser@example.com",
            password="securepassword123",
            first_name="Test",
            last_name="User"
        )
        # URL endpoints - names should match those declared in urls.py
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.register_url = reverse('register')
        self.logout_url = reverse('logout')
        self.user_detail_url = reverse('user_detail')  # View user details endpoint
        self.user_update_url = reverse('user_profile')  # User profile update endpoint

    def authenticate(self):
        """
        Helper method to perform login and set JWT token in HTTP_AUTHORIZATION header.
        This avoids repeating login code in every test that requires authentication.
        """
        response = self.client.post(self.login_url, {
            "username": "testuser",  # Use username as per authentication config
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Ensure login success
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
        # Set token for authenticated requests
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_register_user(self):
        """
        Test user registration endpoint.
        Checks both HTTP status and existence of new user in the DB.
        """
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
        """
        Test logout functionality, typically blacklisting the refresh token.
        Ensures token invalidation returns correct HTTP status.
        """
        self.authenticate()
        response = self.client.post(self.logout_url, {"refresh": self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_user_detail_view(self):
        """
        Test retrieving authenticated user's detail information.
        Checks that email matches the expected value.
        """
        self.authenticate()
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], "testuser@example.com")

    def test_update_user_profile_without_password(self):
        """
        Test updating user profile fields except password.
        Verifies changes are persisted in the database.
        """
        self.authenticate()
        response = self.client.put(self.user_update_url, {
            "first_name": "Updated",
            "last_name": "Name"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()  # Refresh from DB to get updated values
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "Name")

    def test_update_password_with_old_password(self):
        """
        Test password update when the correct old password is provided.
        Ensures password is actually changed and properly hashed.
        """
        self.authenticate()
        response = self.client.put(self.user_update_url, {
            "old_password": "securepassword123",
            "new_password": "newsecurepassword456"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newsecurepassword456"))

    def test_update_password_without_old_password(self):
        """
        Test that password update fails if old password is not provided.
        Checks that API returns HTTP 400 and an error message.
        """
        self.authenticate()
        response = self.client.put(self.user_update_url, {
            "new_password": "newsecurepassword456"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_update_password_with_wrong_old_password(self):
        """
        Test that password update fails if the provided old password is incorrect.
        Confirms error handling and correct HTTP response.
        """
        self.authenticate()
        response = self.client.put(self.user_update_url, {
            "old_password": "wrongpassword",
            "new_password": "newsecurepassword456"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
