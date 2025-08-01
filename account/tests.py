from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from detection.models import PredictionHistory

User = get_user_model()


class AccountTests(APITestCase):
    def setUp(self):
        """
        Create a test user and setup URL reversals.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email="testuser@example.com",
            password="securepassword123",
            first_name="Test",
            last_name="User"
        )
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.register_url = reverse('register')
        self.logout_url = reverse('logout')
        self.user_detail_url = reverse('user_detail')
        self.user_update_url = reverse('user_profile')
        self.user_list_url = reverse('user_list')

    def authenticate(self):
        """
        Log in test user and set Authorization header.
        """
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_register_user(self):
        """
        Should register new user successfully.
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
        Should invalidate refresh token on logout.
        """
        self.authenticate()
        response = self.client.post(self.logout_url, {"refresh": self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_user_detail_view(self):
        """
        Should retrieve logged-in user's profile.
        """
        self.authenticate()
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], "testuser@example.com")

    def test_update_user_profile_without_password(self):
        """
        Should update first/last name without requiring old password.
        """
        self.authenticate()
        response = self.client.put(self.user_update_url, {
            "first_name": "Updated",
            "last_name": "User"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

    def test_update_password_with_old_password(self):
        """
        Should allow password change when correct old password is provided.
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
        Should reject password change if old password is missing.
        """
        self.authenticate()
        response = self.client.put(self.user_update_url, {
            "new_password": "newsecurepassword456"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_update_password_with_wrong_old_password(self):
        """
        Should reject password change if old password is wrong.
        """
        self.authenticate()
        response = self.client.put(self.user_update_url, {
            "old_password": "wrongpassword",
            "new_password": "newsecurepassword456"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_admin_can_view_user_list(self):
        """
        Admin should be able to view the list of all users.
        """
        self.user.is_staff = True
        self.user.save()
        self.authenticate()
        User.objects.create_user(username="another", email="a@example.com", password="pass123")
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(u["username"] == "another" for u in response.data))

    def test_non_admin_cannot_view_user_list(self):
        """
        Regular users should get 403 on user list endpoint.
        """
        self.authenticate()
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_user_prediction_history(self):
        """
        Admin should list all prediction history of a user.
        """
        self.user.is_staff = True
        self.user.save()
        self.authenticate()
        url = reverse('admin-history-list', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_retrieve_single_user_prediction_history(self):
        """
        Admin should fetch a specific prediction entry.
        """
        self.user.is_staff = True
        self.user.save()
        self.authenticate()
        history = PredictionHistory.objects.create(
            user=self.user,
            image='test.jpg',
            disease='Tomato___Late_blight',
            confidence=0.95,
            remedy='Use systemic fungicide.',
            preventive_measures='Rotate crops.'
        )
        url = reverse('admin-history-detail', kwargs={
            'user_id': self.user.id,
            'id': history.id
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['disease'], "Tomato___Late_blight")

    def test_admin_can_delete_single_user_prediction(self):
        """
        Admin should be able to delete a specific prediction.
        """
        self.user.is_staff = True
        self.user.save()
        self.authenticate()
        history = PredictionHistory.objects.create(
            user=self.user,
            image='test.jpg',
            disease='Tomato___Late_blight',
            confidence=0.95,
            remedy='Use systemic fungicide.',
            preventive_measures='Rotate crops.'
        )
        url = reverse('admin-history-delete', kwargs={
            'user_id': self.user.id,
            'id': history.id
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PredictionHistory.objects.filter(id=history.id).exists())

    def test_admin_can_clear_all_user_predictions(self):
        """
        Admin should bulk delete all predictions for a user.
        """
        self.user.is_staff = True
        self.user.save()
        self.authenticate()
        PredictionHistory.objects.bulk_create([
            PredictionHistory(
                user=self.user,
                image='1.jpg',
                disease='Tomato___Early_blight',
                confidence=0.89,
                remedy='Apply fungicide.',
                preventive_measures='Crop rotation.'
            ),
            PredictionHistory(
                user=self.user,
                image='2.jpg',
                disease='Tomato___Late_blight',
                confidence=0.92,
                remedy='Use systemic fungicide.',
                preventive_measures='Avoid overhead watering.'
            ),
        ])
        url = reverse('admin-history-clear', kwargs={'user_id': self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PredictionHistory.objects.filter(user=self.user).count(), 0)
