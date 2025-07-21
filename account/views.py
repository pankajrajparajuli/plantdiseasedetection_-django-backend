from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# account/views.py
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API endpoint that allows new users to register.
    Uses RegisterSerializer to validate and create a new User.
    Permission: AllowAny (no authentication required).
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LogoutView(APIView):
    """
    API endpoint to blacklist refresh token for logout.
    Permission: IsAuthenticated (user must be logged in).
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Accepts a refresh token to blacklist it, effectively logging out the user.
        """
        try:
            refresh_token = request.data["refresh"]  # Get refresh token from request
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token to invalidate it
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            # Return error if token is invalid or missing
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    API endpoint to retrieve details of the currently authenticated user.
    Permission: IsAuthenticated (user must be logged in).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return serialized data of the logged-in user.
        """
        from .serializers import UserSerializer  # Avoid circular import
        serializer = UserSerializer(request.user)  # Serialize user data
        return Response(serializer.data)


class UserProfileUpdateView(APIView):
    """
    API endpoint to update the authenticated user's profile information.
    Supports updating first name, last name, and changing password.

    - Updating first name and last name does NOT require old password.
    - Changing password REQUIRES old password for verification.

    Permission: IsAuthenticated (user must be logged in).
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Handle user profile update including optional password change.
        """
        user = request.user  # Currently logged-in user
        data = request.data  # Incoming update data

        # Update first and last name, defaulting to existing values if not provided
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)

        old_password = data.get('old_password')  # Required if changing password
        new_password = data.get('new_password')  # New password to set

        if new_password:
            # Ensure old password is provided for verification
            if not old_password:
                return Response(
                    {"error": "Old password is required to set a new password."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Verify old password correctness
            if not check_password(old_password, user.password):
                return Response(
                    {"error": "Old password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(new_password)  # Update password if verification passes

        user.save()  # Save changes to database

        return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
