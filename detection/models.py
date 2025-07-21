# models.py

from django.db import models
from django.contrib.auth.models import User


class PredictionHistory(models.Model):
    """
    Model to store history of plant disease predictions made by users.

    Fields:
    - user: ForeignKey to the User who made the prediction.
    - image: Uploaded image of the plant leaf used for prediction.
    - disease: Name of the predicted disease.
    - confidence: Model's confidence score for the prediction.
    - remedy: Suggested remedy for the detected disease.
    - timestamp: Date and time when the prediction was made.
    - preventive_measures: Optional text with prevention advice.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='predicted_images/')
    disease = models.CharField(max_length=100)
    confidence = models.FloatField()
    remedy = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    preventive_measures = models.TextField(blank=True, null=True)

    def __str__(self):
        """String representation showing user, disease, confidence and timestamp."""
        return f"{self.user.username} - {self.disease} - {self.confidence:.2f} - {self.timestamp}"
