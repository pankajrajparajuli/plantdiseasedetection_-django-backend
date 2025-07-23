from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

"""
URL patterns for user account-related API endpoints.

Includes registration, login, token refresh, profile update,
user detail retrieval, and logout endpoints.
"""

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),  # List all users (admin only)
    path('register/', RegisterView.as_view(), name='register'),  # User registration endpoint
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT login endpoint
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT token refresh endpoint
    path('update_profile/', UserProfileUpdateView.as_view(), name='user_profile'),  # User profile update endpoint
    path('user_detail/', UserDetailView.as_view(), name='user_detail'),  # Get authenticated user details
    path('logout/', LogoutView.as_view(), name='logout'),  # User logout endpoint (token blacklist)
    path('users/<int:user_id>/history/', AdminUserHistoryView.as_view(), name='admin-history-list'),
    path('users/<int:user_id>/history/<int:id>/', AdminUserHistoryView.as_view(), name='admin-history-detail'),
    path('users/<int:user_id>/history/<int:id>/delete/', AdminUserHistoryView.as_view(), name='admin-history-delete'),
    path('users/<int:user_id>/history/clear/', AdminUserHistoryClearView.as_view(), name='admin-history-clear'),
]
# This file defines the URL patterns for the account app, linking views to specific endpoints.