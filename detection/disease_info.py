# This file contains predefined remedies and preventive measures for each plant disease label.
# It's separated for cleaner views logic and easy maintenance.

# List of labels the model can predict
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

# Remedies dictionary: suggested treatment for detected disease
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
    'Tomato___healthy': 'No disease detected.',
}

# Preventive measures dictionary: how to avoid the disease in future
preventive_measures = {
    'Apple___Apple_scab': 'Ensure good air circulation and sanitation. Prune regularly and remove fallen leaves.',
    'Apple___Black_rot': 'Avoid overhead watering. Clean pruning tools and remove nearby infected debris.',
    'Apple___Cedar_apple_rust': 'Avoid planting apples near cedar trees. Spray fungicides in early season.',
    'Apple___healthy': 'Continue proper pruning and sanitation to prevent diseases.',

    'Blueberry___healthy': 'Maintain proper watering and spacing to avoid future diseases.',

    'Cherry_(including_sour)___Powdery_mildew': 'Ensure good airflow. Water early in the day and avoid leaf wetting.',
    'Cherry_(including_sour)___healthy': 'Regular pruning and mulching will help maintain plant health.',

    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 'Rotate crops, use resistant hybrids, and avoid dense planting.',
    'Corn_(maize)___Common_rust_': 'Avoid excessive nitrogen. Remove crop debris after harvest.',
    'Corn_(maize)___Northern_Leaf_Blight': 'Use certified seed and rotate with non-host crops.',
    'Corn_(maize)___healthy': 'Continue using disease-free seeds and proper irrigation.',

    'Grape___Black_rot': 'Prune properly and dispose of infected parts. Avoid overhead irrigation.',
    'Grape___Esca_(Black_Measles)': 'Avoid pruning in wet weather and disinfect tools.',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 'Avoid wet foliage. Ensure adequate spacing between vines.',
    'Grape___healthy': 'Good pruning and fungicide schedule keeps grape vines healthy.',

    'Orange___Haunglongbing_(Citrus_greening)': 'Use certified disease-free planting material. Monitor insect pests regularly.',

    'Peach___Bacterial_spot': 'Plant resistant varieties. Avoid handling when wet.',
    'Peach___healthy': 'Continue good hygiene and monitor for symptoms regularly.',

    'Pepper,_bell___Bacterial_spot': 'Use raised beds and avoid overcrowding. Sterilize equipment.',
    'Pepper,_bell___healthy': 'Maintain proper drainage and space between plants.',

    'Potato___Early_blight': 'Rotate crops and avoid planting potatoes where tomatoes grew previously.',
    'Potato___Late_blight': 'Remove volunteers and avoid overhead irrigation.',
    'Potato___healthy': 'Monitor soil drainage and rotate crops regularly.',

    'Raspberry___healthy': 'Avoid overhead irrigation and prune old canes regularly.',

    'Soybean___healthy': 'Ensure proper planting density and pest monitoring.',

    'Squash___Powdery_mildew': 'Water at base of plant and avoid excessive nitrogen application.',

    'Strawberry___Leaf_scorch': 'Ensure adequate spacing, and remove infected leaves promptly.',
    'Strawberry___healthy': 'Rotate planting sites and remove weeds around strawberry beds.',

    'Tomato___Bacterial_spot': 'Avoid working in wet fields and sterilize tools.',
    'Tomato___Early_blight': 'Use mulch to reduce soil splash. Remove lower infected leaves.',
    'Tomato___Late_blight': 'Plant in full sun and avoid waterlogged soils.',
    'Tomato___Leaf_Mold': 'Provide good ventilation and avoid water on leaves.',
    'Tomato___Septoria_leaf_spot': 'Avoid overhead watering and remove weeds around tomatoes.',
    'Tomato___Spider_mites Two-spotted_spider_mite': 'Spray water to dislodge mites and control dust around plants.',
    'Tomato___Target_Spot': 'Use resistant varieties and avoid plant injury.',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'Use insect-proof nets and virus-free transplants.',
    'Tomato___Tomato_mosaic_virus': 'Disinfect tools, avoid handling plants when smoking.',
    'Tomato___healthy': 'Maintain regular crop inspection and good cultural practices.',
}

# Default messages in case a label is not found in the dictionary
default_remedy = "Use recommended fungicides and practice good agricultural hygiene."
default_prevention = "Ensure proper spacing, crop rotation, watering practices, and hygiene."
# List of all possible labels for validation