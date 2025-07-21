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


# API view for predicting plant disease from an uploaded image
class PlantDiseaseDetectAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only accessible to logged-in users

    def post(self, request):
        # Ensure the request contains an image
        if 'image' not in request.FILES:
            return Response({"error": "No leaf or disease found. Please provide a leaf image."},
                            status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']

        try:
            # Preprocess the image
            img = Image.open(image_file).convert('RGB')
            img = img.resize((224, 224))  # Resize to match model input
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            model = get_model()

            # Make prediction
            preds = model.predict(img_array)
            pred_class = int(np.argmax(preds))
            pred_label = label_list[pred_class]
            confidence = float(np.max(preds))
            remedy = remedies.get(pred_label, default_remedy)
            prevention = preventive_measures.get(pred_label, "No specific prevention measures available.")

            # Save prediction to DB for the authenticated user
            if request.user.is_authenticated:
                PredictionHistory.objects.create(
                    user=request.user,
                    image=image_file,
                    disease=pred_label,
                    confidence=confidence,
                    remedy=remedy
                )

            return Response({
                "disease": pred_label,
                "confidence": round(confidence, 4),
                "remedy": remedy,
                "prevention": prevention,
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API to list all past predictions of the logged-in user
class HistoryListView(generics.ListAPIView):
    serializer_class = PredictionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PredictionHistory.objects.filter(user=self.request.user).order_by('-timestamp')


# API to retrieve specific prediction detail
class HistoryDetailView(generics.RetrieveAPIView):
    serializer_class = PredictionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return PredictionHistory.objects.filter(user=self.request.user)


# API to delete specific prediction history
class HistoryDeleteView(generics.DestroyAPIView):
    serializer_class = PredictionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return PredictionHistory.objects.filter(user=self.request.user)


# This view handles deletion of all prediction history for the authenticated user
class ClearHistoryView(APIView):
    # Only allow access to authenticated users
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        # Get the password from the request data
        password = request.data.get("password")

        # If password is not provided, return 400 Bad Request
        if not password:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the provided password matches the user's password
        if not check_password(password, request.user.password):
            # If password is incorrect, return 403 Forbidden
            return Response({"error": "Incorrect password."}, status=status.HTTP_403_FORBIDDEN)

        # Delete all prediction history records for the current user
        deleted_count, _ = PredictionHistory.objects.filter(user=request.user).delete()

        # Return a success response with the number of deleted records
        return Response({"message": f"{deleted_count} records deleted."}, status=status.HTTP_204_NO_CONTENT)
