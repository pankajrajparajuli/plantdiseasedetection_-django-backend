from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from PIL import Image
import numpy as np
import tensorflow as tf
from .models import PredictionHistory
from .serializers import PredictionHistorySerializer
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # path to project root
model_path = os.path.join(BASE_DIR, 'cnn_model', 'plant_disease_prediction_model.h5')

model = tf.keras.models.load_model(model_path)

# Ensure the model is loaded correctly

label_list = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

remedies = {
    'Apple___Apple_scab': 'Use fungicides like captan or mancozeb and remove infected leaves.',
    'Apple___Black_rot': 'Prune out infected limbs and apply fungicides during the growing season.',
    'Apple___Cedar_apple_rust': 'Apply fungicides early in the season and remove nearby cedar trees if possible.',
    'Apple___healthy': 'No disease detected.',

    'Blueberry___healthy': 'No disease detected.',

    'Cherry_(including_sour)___Powdery_mildew': 'Use sulfur-based fungicides and prune affected areas.',
    'Cherry_(including_sour)___healthy': 'No disease detected.',

    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 'Rotate crops, use resistant hybrids, and apply fungicides.',
    'Corn_(maize)___Common_rust_': 'Use resistant varieties and apply fungicides at early stages.',
    'Corn_(maize)___Northern_Leaf_Blight': 'Use resistant hybrids and apply fungicides if disease pressure is high.',
    'Corn_(maize)___healthy': 'No disease detected.',

    'Grape___Black_rot': 'Use fungicides and remove mummified fruit and infected leaves.',
    'Grape___Esca_(Black_Measles)': 'Avoid pruning during wet conditions and remove infected vines.',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 'Apply copper-based fungicides and prune affected leaves.',
    'Grape___healthy': 'No disease detected.',

    'Orange___Haunglongbing_(Citrus_greening)': 'Remove infected trees and control psyllid insects with insecticides.',

    'Peach___Bacterial_spot': 'Use resistant varieties and copper-based sprays during early growth stages.',
    'Peach___healthy': 'No disease detected.',

    'Pepper,_bell___Bacterial_spot': 'Use disease-free seeds and copper-based fungicides. Avoid overhead watering.',
    'Pepper,_bell___healthy': 'No disease detected.',

    'Potato___Early_blight': 'Use certified seed and apply fungicides like chlorothalonil or mancozeb.',
    'Potato___Late_blight': 'Destroy infected plants and apply systemic fungicides like metalaxyl.',
    'Potato___healthy': 'No disease detected.',

    'Raspberry___healthy': 'No disease detected.',

    'Soybean___healthy': 'No disease detected.',

    'Squash___Powdery_mildew': 'Apply sulfur-based or systemic fungicides like myclobutanil.',

    'Strawberry___Leaf_scorch': 'Remove infected leaves and apply fungicides such as captan.',
    'Strawberry___healthy': 'No disease detected.',

    'Tomato___Bacterial_spot': 'Use copper-based sprays and disease-free seeds.',
    'Tomato___Early_blight': 'Use crop rotation and apply fungicides like chlorothalonil or mancozeb.',
    'Tomato___Late_blight': 'Apply systemic fungicides and remove infected plants promptly.',
    'Tomato___Leaf_Mold': 'Ensure good air circulation and apply fungicides such as mancozeb.',
    'Tomato___Septoria_leaf_spot': 'Remove infected leaves and apply fungicides like chlorothalonil.',
    'Tomato___Spider_mites Two-spotted_spider_mite': 'Use miticides or insecticidal soap. Maintain proper moisture.',
    'Tomato___Target_Spot': 'Apply preventive fungicides and practice crop rotation.',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'Control whiteflies and use resistant tomato varieties.',
    'Tomato___Tomato_mosaic_virus': 'Disinfect tools and avoid smoking near plants. No chemical cure.',
    'Tomato___healthy': 'No disease detected.'
}

default_remedy = "Use recommended fungicides and practice good agricultural hygiene."


class PlantDiseaseDetectAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Require login

    def post(self, request):
        if 'image' not in request.FILES:
            return Response({"error": "No leaf or disease found. Please provide a leaf image."},
                            status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']

        try:
            img = Image.open(image_file).convert('RGB')
            img = img.resize((224, 224))  # Match training size
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            preds = model.predict(img_array)
            pred_class = int(np.argmax(preds))
            pred_label = label_list[pred_class]
            confidence = float(np.max(preds))
            remedy = remedies.get(pred_label, default_remedy)

            # Save to DB only if user is authenticated
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
                "remedy": remedy
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HistoryListView(generics.ListAPIView):
    serializer_class = PredictionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PredictionHistory.objects.filter(user=self.request.user)


class HistoryDetailView(generics.RetrieveAPIView):
    serializer_class = PredictionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return PredictionHistory.objects.filter(user=self.request.user)


class HistoryDeleteView(generics.DestroyAPIView):
    serializer_class = PredictionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return PredictionHistory.objects.filter(user=self.request.user)


class ClearHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        deleted_count, _ = PredictionHistory.objects.filter(user=request.user).delete()
        return Response({"message": f"{deleted_count} records deleted."}, status=status.HTTP_204_NO_CONTENT)
