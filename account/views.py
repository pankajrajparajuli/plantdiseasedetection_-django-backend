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
    Permission: AllowAny (no authentication required)
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)  # user must be logged in

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # blacklist the refresh token
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    API endpoint to retrieve details of the currently authenticated user.
    Returns user data serialized by UserSerializer.
    Permission: IsAuthenticated (user must be logged in)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Import serializer here to avoid circular imports
        from .serializers import UserSerializer

        # Serialize the current user data
        serializer = UserSerializer(request.user)
        # Return serialized user data in response
        return Response(serializer.data)


class UserProfileUpdateView(APIView):
    """
    API endpoint to update the authenticated user's profile information.
    Supports updating first name, last name, and changing password.

    - Updating first name and last name does NOT require old password.
    - Changing password REQUIRES old password for verification.

    Permission: IsAuthenticated (user must be logged in)
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user  # Get currently logged-in user
        data = request.data  # Get data sent in request body

        # Update first name and last name directly without needing old password
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)

        old_password = data.get('old_password')  # Old password for verification if changing password
        new_password = data.get('new_password')  # New password user wants to set

        # If user wants to change password
        if new_password:
            # Check if old password was provided
            if not old_password:
                # Return error if old password missing
                return Response(
                    {"error": "Old password is required to set a new password."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Verify that old password is correct
            if not check_password(old_password, user.password):
                # Return error if old password is incorrect
                return Response(
                    {"error": "Old password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Set new password if verification passed
            user.set_password(new_password)

        user.save()  # Save updated user info to the database

        # Return success message after update
        return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
