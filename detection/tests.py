from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from detection.models import PredictionHistory
from io import BytesIO
from PIL import Image

User = get_user_model()


class DetectionTests(APITestCase):
    def setUp(self):
        """
        Set up a user and authenticate them for protected endpoints.
        """
        self.user = User.objects.create_user(
            username='leafuser',
            email='leaf@example.com',
            password='leafpass123'
        )
        self.login_url = reverse('token_obtain_pair')
        self.predict_url = reverse('predict')
        self.history_list_url = reverse('history-list')
        self.clear_history_url = reverse('history-clear')

        # Authenticate
        response = self.client.post(self.login_url, {
            "username": "leafuser",
            "password": "leafpass123"
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def generate_test_image(self):
        """
        Generates a basic in-memory green image for testing.
        """
        img = Image.new('RGB', (224, 224), color='green')
        file = BytesIO()
        img.save(file, 'jpeg')
        file.name = 'test.jpg'
        file.seek(0)
        return file

    def test_predict_disease_from_image(self):
        """
        Should return disease label and info after uploading an image.
        """
        image = self.generate_test_image()
        response = self.client.post(self.predict_url, {'image': image}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('disease', response.data)
        self.assertIn('remedy', response.data)
        self.assertIn('preventive_measure', response.data)

    def test_history_list(self):
        """
        Should return prediction history for the user.
        """
        PredictionHistory.objects.create(
            user=self.user,
            image='img.jpg',
            disease='Tomato___Late_blight',
            confidence=0.91,
            remedy='Fungicide',
            preventive_measures='Crop rotation'
        )
        response = self.client.get(self.history_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_history_detail(self):
        """
        Should return details of a single prediction.
        """
        history = PredictionHistory.objects.create(
            user=self.user,
            image='img.jpg',
            disease='Tomato___Early_blight',
            confidence=0.85,
            remedy='Use fungicide',
            preventive_measures='Crop rotation'
        )
        url = reverse('history-detail', kwargs={'id': history.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['disease'], 'Tomato___Early_blight')

    def test_history_delete(self):
        """
        Should delete a specific prediction from history.
        """
        history = PredictionHistory.objects.create(
            user=self.user,
            image='img.jpg',
            disease='Tomato___Leaf_Mold',
            confidence=0.8,
            remedy='Fungicide',
            preventive_measures='Ventilation'
        )
        url = reverse('history-delete', kwargs={'id': history.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PredictionHistory.objects.filter(id=history.id).exists())

    def test_clear_all_history_with_password(self):
        """
        Should clear all predictions when correct password is provided.
        """
        PredictionHistory.objects.create(
            user=self.user,
            image='img.jpg',
            disease='Tomato___Early_blight',
            confidence=0.75,
            remedy='Fungicide',
            preventive_measures='Spacing'
        )
        response = self.client.delete(self.clear_history_url, {
            'password': 'leafpass123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PredictionHistory.objects.filter(user=self.user).count(), 0)

    def test_clear_history_wrong_password(self):
        """
        Should return 403 Forbidden if wrong password is used.
        """
        response = self.client.delete(self.clear_history_url, {
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
