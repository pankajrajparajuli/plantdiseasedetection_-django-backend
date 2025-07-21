from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

"""
URL patterns for user account-related API endpoints.

Includes registration, login, token refresh, profile update,
user detail retrieval, and logout endpoints.
"""

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # User registration endpoint
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT login endpoint
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT token refresh endpoint
    path('update_profile/', UserProfileUpdateView.as_view(), name='user_profile'),  # User profile update endpoint
    path('user_detail/', UserDetailView.as_view(), name='user_detail'),  # Get authenticated user details
    path('logout/', LogoutView.as_view(), name='logout'),  # User logout endpoint (token blacklist)
]
# This file defines the URL patterns for the account app, linking views to specific endpoints.