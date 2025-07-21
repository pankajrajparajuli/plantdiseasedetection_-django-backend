from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from io import BytesIO
from PIL import Image
from .models import PredictionHistory

User = get_user_model()


def create_test_image():
    """
    Helper function to create an in-memory image file for upload testing.
    Avoids filesystem dependencies and speeds up tests.
    """
    img = Image.new('RGB', (224, 224), color='green')
    temp_file = BytesIO()
    img.save(temp_file, format='JPEG')
    temp_file.name = 'test.jpg'  # Important for DRF to recognize file name
    temp_file.seek(0)
    return temp_file


class PlantDiseaseDetectionTests(APITestCase):
    def setUp(self):
        """
        Prepare test user and authenticate using JWT tokens.
        This simulates a real client obtaining and using JWT for authenticated requests.
        Also sets URL variables based on your urls.py 'name' attributes.
        """
        # Create user
        self.user = User.objects.create_user(username='testuser', password='pass1234')

        # Obtain JWT token via login endpoint
        token_url = reverse('token_obtain_pair')  # Adjust if your JWT login url name differs
        response = self.client.post(token_url, {'username': 'testuser', 'password': 'pass1234'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Token obtain failed during setup")

        # Save token and set Authorization header for all requests
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Store URL paths for easy reuse in tests
        self.detect_url = reverse('predict')
        self.history_list_url = reverse('history-list')
        self.clear_history_url = reverse('history-clear')

    def test_predict_success(self):
        """
        Verify that uploading a valid image triggers successful prediction.
        Checks response fields and database record creation.
        """
        image = create_test_image()
        response = self.client.post(self.detect_url, {'image': image}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validate presence of key response data fields
        self.assertIn('disease', response.data)
        self.assertIn('confidence', response.data)
        self.assertIn('remedy', response.data)
        self.assertIn('prevention', response.data)

        # Confirm prediction history record created for current user
        self.assertTrue(PredictionHistory.objects.filter(user=self.user).exists())

    def test_predict_no_image(self):
        """
        Ensure endpoint returns 400 Bad Request if image is missing.
        """
        response = self.client.post(self.detect_url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_history_list_authenticated(self):
        """
        Test retrieval of prediction history list for authenticated user.
        Checks that at least one record is returned after creation.
        """
        # Create a sample history record for user
        PredictionHistory.objects.create(
            user=self.user,
            disease='Test Disease',
            confidence=0.9,
            remedy='Test remedy'
        )
        response = self.client.get(self.history_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_history_list_unauthenticated(self):
        """
        Verify unauthenticated users cannot access history list.
        Should return 401 Unauthorized.
        """
        self.client.credentials()  # Clear credentials to simulate unauthenticated request
        response = self.client.get(self.history_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_history_detail_view(self):
        """
        Test retrieval of specific prediction history by ID.
        Confirms 200 OK and matching ID in response.
        """
        history = PredictionHistory.objects.create(
            user=self.user,
            disease='Test Disease',
            confidence=0.9,
            remedy='Test remedy'
        )
        url = reverse('history-detail', kwargs={'id': history.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], history.id)

    def test_history_delete_view(self):
        """
        Test deletion of a specific prediction history record.
        Checks for 204 No Content and confirms deletion.
        """
        history = PredictionHistory.objects.create(
            user=self.user,
            disease='Test Disease',
            confidence=0.9,
            remedy='Test remedy'
        )
        url = reverse('history-delete', kwargs={'id': history.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PredictionHistory.objects.filter(id=history.id).exists())

    def test_clear_history_no_password(self):
        """
        Validate clear history endpoint rejects requests missing password.
        Returns 400 Bad Request with error message.
        """
        response = self.client.delete(self.clear_history_url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_clear_history_wrong_password(self):
        """
        Validate clear history endpoint rejects requests with wrong password.
        Returns 403 Forbidden with error message.
        """
        response = self.client.delete(self.clear_history_url, data={'password': 'wrongpass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('error', response.data)

    def test_clear_history_success(self):
        """
        Test successful deletion of all prediction history when correct password is provided.
        Confirms 204 No Content and empty history afterwards.
        """
        # Create some history entries for user
        PredictionHistory.objects.create(
            user=self.user,
            disease='Test Disease',
            confidence=0.9,
            remedy='Test remedy'
        )
        response = self.client.delete(self.clear_history_url, data={'password': 'pass1234'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PredictionHistory.objects.filter(user=self.user).count(), 0)
