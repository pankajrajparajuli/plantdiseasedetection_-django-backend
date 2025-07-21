# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='predicted_images/')
    disease = models.CharField(max_length=100)
    confidence = models.FloatField()
    remedy = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    preventive_measures = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.disease} - {self.confidence:.2f} - {self.timestamp}"
