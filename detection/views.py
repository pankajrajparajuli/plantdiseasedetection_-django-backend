from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from PIL import Image
import numpy as np
from .models import PredictionHistory
from .serializers import PredictionHistorySerializer
from .disease_info import label_list, remedies, default_remedy, preventive_measures
from .model_loader import get_model
from django.contrib.auth.hashers import check_password


class PlantDiseaseDetectAPIView(APIView):
    """
    API endpoint for predicting plant disease from an uploaded leaf image.
    Only accessible to authenticated users.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle POST request with image file, run prediction, save to DB, and return results.
        """
        # Validate presence of image file in request
        if 'image' not in request.FILES:
            return Response(
                {"error": "No leaf or disease found. Please provide a leaf image."},
                status=status.HTTP_400_BAD_REQUEST
            )

        image_file = request.FILES['image']

        try:
            # Load and preprocess image for model input
            img = Image.open(image_file).convert('RGB')
            img = img.resize((224, 224))  # Resize image to model expected input size
            img_array = np.array(img) / 255.0  # Normalize pixel values
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

            # Load ML model and get prediction
            model = get_model()
            preds = model.predict(img_array)
            pred_class = int(np.argmax(preds))
            pred_label = label_list[pred_class]
            confidence = float(np.max(preds))

            # Retrieve remedy and prevention info for predicted disease
            remedy = remedies.get(pred_label, default_remedy)
            prevention = preventive_measures.get(pred_label, "No specific prevention measures available.")

            # Save prediction record if user is authenticated
            if request.user.is_authenticated:
                PredictionHistory.objects.create(
                    user=request.user,
                    image=image_file,
                    disease=pred_label,
                    confidence=confidence,
                    remedy=remedy
                )

            # Return prediction response
            return Response({
                "disease": pred_label,
                "confidence": round(confidence, 4),
                "remedy": remedy,
                "prevention": prevention,
            })

        except Exception as e:
            # Return error response on failure
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HistoryListView(generics.ListAPIView):
    """
    API endpoint to list all past prediction histories of the authenticated user.
    """
    serializer_class = PredictionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return user's predictions ordered by newest first
        return PredictionHistory.objects.filter(user=self.request.user).order_by('-timestamp')


class HistoryDetailView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve detailed information of a specific prediction.
    """
    serializer_class = PredictionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        # Ensure user can only access their own prediction history
        return PredictionHistory.objects.filter(user=self.request.user)


class HistoryDeleteView(generics.DestroyAPIView):
    """
    API endpoint to delete a specific prediction history entry.
    """
    serializer_class = PredictionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        # Restrict deletion to authenticated user's own history entries
        return PredictionHistory.objects.filter(user=self.request.user)


class ClearHistoryView(APIView):
    """
    API endpoint to delete all prediction history for the authenticated user.
    Requires user password confirmation for security.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        """
        Handle DELETE request to clear all user's prediction history after password verification.
        """
        password = request.data.get("password")

        if not password:
            # Password must be provided
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the provided password is correct
        if not check_password(password, request.user.password):
            return Response({"error": "Incorrect password."}, status=status.HTTP_403_FORBIDDEN)

        # Delete all prediction history objects for the user
        deleted_count, _ = PredictionHistory.objects.filter(user=request.user).delete()

        # Respond with number of deleted records
        return Response({"message": f"{deleted_count} records deleted."}, status=status.HTTP_204_NO_CONTENT)
# This file defines the views for the detection app, handling plant disease prediction and history management.
# It includes endpoints for disease detection, listing history, viewing details, deleting entries, and clearing history.
