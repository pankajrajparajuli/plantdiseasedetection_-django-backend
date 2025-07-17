from django.urls import path
from .views import PlantDiseaseDetectAPIView, HistoryListView, HistoryDetailView, HistoryDeleteView, ClearHistoryView

urlpatterns = [
    path('predict/', PlantDiseaseDetectAPIView.as_view(), name='predict'),
    path('history/', HistoryListView.as_view(), name='history-list'),
    path('history/<int:id>/', HistoryDetailView.as_view(), name='history-detail'),
    path('history/<int:id>/delete/', HistoryDeleteView.as_view(), name='history-delete'),
    path('history/clear/', ClearHistoryView.as_view(), name='history-clear'),
]
# This file defines the URL patterns for the detection app, linking views to specific endpoints.