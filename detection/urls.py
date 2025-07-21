from django.urls import path
from .views import (
    PlantDiseaseDetectAPIView,  # Prediction endpoint
    HistoryListView,  # List all prediction history for user
    HistoryDetailView,  # Retrieve detail of a single history record
    HistoryDeleteView,  # Delete a single history record
    ClearHistoryView,  # Delete all history records for the user
)

urlpatterns = [
    path('predict/', PlantDiseaseDetectAPIView.as_view(), name='predict'),  # Predict disease from image
    path('history/', HistoryListView.as_view(), name='history-list'),  # List user's prediction history
    path('history/<int:id>/', HistoryDetailView.as_view(), name='history-detail'),  # Get detail of one prediction
    path('history/<int:id>/delete/', HistoryDeleteView.as_view(), name='history-delete'),  # Delete one prediction record
    path('history/clear/', ClearHistoryView.as_view(), name='history-clear'),  # Delete all prediction history for user
]
# This file defines the URL patterns for the detection app, linking views to specific endpoints.
