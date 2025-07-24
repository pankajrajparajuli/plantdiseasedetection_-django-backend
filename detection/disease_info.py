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
    'Apple___Apple_scab': 'Apply fungicides like captan or mancozeb during the early stages of infection. Remove and destroy infected leaves to prevent further spread. Maintain regular pruning to improve airflow and reduce moisture.',
    'Apple___Black_rot': 'Prune out all infected limbs and twigs during the dormant season. Apply fungicides throughout the growing season as needed. Remove fallen fruit and debris to minimize reinfection risk.',
    'Apple___Cedar_apple_rust': 'Use preventive fungicides at the beginning of the growing season. Remove nearby cedar trees to reduce spore sources. Monitor and prune affected areas regularly to maintain tree health.',
    'Apple___healthy': 'Your apple plant shows no signs of disease. Continue regular care practices like pruning and balanced fertilization. Monitor the plant routinely for any changes.',

    'Blueberry___healthy': 'Your blueberry plant is currently healthy. Maintain proper watering and avoid overcrowding to prevent disease development. Regularly inspect for pests or early symptoms.',

    'Cherry_(including_sour)___Powdery_mildew': 'Apply sulfur-based fungicides early in the season to control fungal growth. Prune affected branches to improve airflow. Water the base of the plant to keep foliage dry.',
    'Cherry_(including_sour)___healthy': 'No disease detected. Continue good watering practices and regular pruning to prevent future problems. Monitor for any changes in leaf color or growth.',

    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 'Rotate crops annually to break the disease cycle. Use resistant hybrids for better protection. Apply fungicides when disease pressure is high.',
    'Corn_(maize)___Common_rust_': 'Plant resistant corn varieties to minimize infection risk. Apply fungicides during the early growth stages if necessary. Maintain proper spacing to reduce humidity between plants.',
    'Corn_(maize)___Northern_Leaf_Blight': 'Choose resistant corn hybrids for long-term management. Use fungicides at the first sign of symptoms. Remove crop debris after harvest to reduce overwintering spores.',
    'Corn_(maize)___healthy': 'Your corn plant is currently healthy. Maintain good field hygiene and crop rotation practices. Monitor regularly to catch any early signs of disease.',

    'Grape___Black_rot': 'Apply fungicides throughout the growing season as a preventive measure. Remove all mummified fruit and infected leaves. Ensure good airflow by pruning excess growth.',
    'Grape___Esca_(Black_Measles)': 'Avoid pruning during wet conditions to prevent infections. Remove and destroy any infected vines promptly. Use fungicides as part of a comprehensive vineyard management plan.',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 'Apply copper-based fungicides to control infection spread. Prune and dispose of affected leaves carefully. Maintain proper spacing to reduce excess moisture.',
    'Grape___healthy': 'Your grapevine is currently in good condition. Maintain a regular fungicide schedule for prevention. Prune and train vines for optimal air circulation.',

    'Orange___Haunglongbing_(Citrus_greening)': 'Remove and destroy infected trees to prevent further spread. Control psyllid insect populations using approved insecticides. Monitor regularly for early symptoms of reinfection.',

    'Peach___Bacterial_spot': 'Plant resistant peach varieties whenever possible. Apply copper-based sprays during early growth stages. Avoid overhead irrigation to reduce leaf wetness.',
    'Peach___healthy': 'Your peach plant is currently disease-free. Keep practicing good sanitation and pruning methods. Monitor for any signs of bacterial spots during growth.',

    'Pepper,_bell___Bacterial_spot': 'Use disease-free seeds to prevent introducing pathogens. Apply copper-based fungicides as needed. Avoid overhead watering to keep foliage dry.',
    'Pepper,_bell___healthy': 'Your pepper plant is in excellent condition. Maintain proper watering and balanced fertilization. Regularly check for pests or leaf discoloration.',

    'Potato___Early_blight': 'Use certified disease-free seed potatoes. Apply fungicides such as chlorothalonil or mancozeb when symptoms appear. Remove and destroy affected foliage to prevent further spread.',
    'Potato___Late_blight': 'Destroy infected plants immediately to stop the disease. Apply systemic fungicides like metalaxyl for better control. Avoid planting potatoes near tomatoes to minimize risk.',
    'Potato___healthy': 'Your potato crop is currently healthy. Maintain proper soil drainage and avoid waterlogging. Continue crop rotation practices for long-term prevention.',

    'Raspberry___healthy': 'Your raspberry plant is doing well. Prune old canes regularly to improve airflow. Monitor for pests or any changes in leaf color.',

    'Soybean___healthy': 'Your soybean crop appears healthy. Use proper planting density to maintain air circulation. Regularly monitor for pests and potential infections.',

    'Squash___Powdery_mildew': 'Apply sulfur-based or systemic fungicides at the first sign of mildew. Water at the plant’s base to keep leaves dry. Remove infected foliage to prevent further spread.',

    'Strawberry___Leaf_scorch': 'Remove infected leaves promptly to stop the spread. Apply protective fungicides such as captan as needed. Ensure plants are spaced well for airflow.',
    'Strawberry___healthy': 'Your strawberry plants are healthy. Rotate planting sites to reduce disease risk. Maintain weed-free beds and proper irrigation practices.',

    'Tomato___Bacterial_spot': 'Use copper-based sprays to control bacterial infections. Plant disease-free seeds or seedlings for prevention. Avoid working with plants when they are wet.',
    'Tomato___Early_blight': 'Rotate crops to reduce soil-borne pathogens. Apply fungicides like chlorothalonil or mancozeb as needed. Remove and destroy infected lower leaves.',
    'Tomato___Late_blight': 'Apply systemic fungicides for effective control. Remove and dispose of infected plants immediately. Ensure proper spacing for good air circulation.',
    'Tomato___Leaf_Mold': 'Increase ventilation in growing areas to reduce humidity. Apply fungicides such as mancozeb if necessary. Remove infected leaves promptly.',
    'Tomato___Septoria_leaf_spot': 'Remove and destroy infected leaves to slow the disease. Apply protective fungicides like chlorothalonil. Keep foliage dry by avoiding overhead watering.',
    'Tomato___Spider_mites Two-spotted_spider_mite': 'Spray water to dislodge mites from the leaves. Use miticides or insecticidal soaps for control. Maintain proper plant moisture to discourage mite infestations.',
    'Tomato___Target_Spot': 'Apply preventive fungicides to control fungal growth. Rotate crops to reduce recurring infections. Remove damaged leaves to maintain plant health.',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'Control whitefly populations using insecticides or traps. Plant resistant tomato varieties for better protection. Use row covers or nets to reduce insect exposure.',
    'Tomato___Tomato_mosaic_virus': 'Disinfect all tools before and after working with infected plants. Avoid smoking or handling tobacco near tomato plants. Remove and destroy severely infected plants.',
    'Tomato___healthy': 'Your tomato plants are healthy. Maintain regular inspections to catch early signs of problems. Use balanced fertilizers and proper irrigation for sustained growth.',
}
preventive_measures = {
    'Apple___Apple_scab': 'Prune apple trees regularly to improve airflow and reduce humidity. Remove and destroy fallen leaves and debris that may harbor fungal spores. Apply preventive fungicides during the early spring season for better protection.',
    'Apple___Black_rot': 'Avoid overhead watering to reduce leaf wetness and fungal growth. Always clean pruning tools before and after use to prevent spreading the disease. Remove infected branches and nearby plant debris promptly.',
    'Apple___Cedar_apple_rust': 'Do not plant apple trees near cedar trees, as they can host rust spores. Use preventive fungicides early in the growing season to protect new growth. Inspect leaves regularly for rust-colored spots and take immediate action if detected.',
    'Apple___healthy': 'Maintain consistent pruning and sanitation practices throughout the year. Keep the orchard floor free from fallen leaves and decayed fruits. Continue using seasonal preventive fungicide sprays for added protection.',

    'Blueberry___healthy': 'Space blueberry bushes properly to promote airflow and reduce disease risk. Water at the base of the plant to keep foliage dry and prevent fungal issues. Apply mulch to maintain soil moisture and suppress weeds.',

    'Cherry_(including_sour)___Powdery_mildew': 'Prune cherry trees to ensure good airflow and sunlight penetration. Water early in the day to allow leaves to dry quickly and reduce fungal infection risk. Apply preventive fungicides as soon as symptoms are noticed.',
    'Cherry_(including_sour)___healthy': 'Continue regular pruning to maintain tree health and shape. Mulch around the base to preserve soil moisture and control weeds. Monitor leaves frequently for any signs of disease.',

    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 'Rotate corn with non-host crops to break the disease cycle. Choose disease-resistant hybrids to minimize infection risks. Avoid dense planting to ensure proper airflow between plants.',
    'Corn_(maize)___Common_rust_': 'Do not overuse nitrogen fertilizers, as excess can increase susceptibility. Remove crop debris after harvest to reduce overwintering of rust spores. Monitor regularly and apply fungicides if disease pressure is high.',
    'Corn_(maize)___Northern_Leaf_Blight': 'Use certified, disease-free seeds for planting. Rotate corn with non-host crops to prevent pathogen buildup in the soil. Monitor fields early in the season and apply fungicides if symptoms develop.',
    'Corn_(maize)___healthy': 'Continue planting high-quality seeds and maintaining proper irrigation practices. Rotate crops regularly to reduce the risk of disease buildup. Keep an eye on leaf health and address any changes early.',

    'Grape___Black_rot': 'Prune vines properly to improve air circulation and sunlight penetration. Remove any infected fruit and leaves promptly to reduce disease sources. Avoid overhead irrigation to keep foliage dry and minimize infection.',
    'Grape___Esca_(Black_Measles)': 'Avoid pruning grapevines during wet weather to reduce infection chances. Disinfect pruning tools before and after use to prevent spreading pathogens. Remove severely infected vines to protect the rest of the vineyard.',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 'Maintain proper vine spacing to improve airflow and reduce leaf wetness. Avoid overhead watering to keep foliage dry. Apply preventive fungicides before rainy periods to minimize disease development.',
    'Grape___healthy': 'Continue regular pruning and training to maintain healthy vine structure. Apply preventive fungicide treatments as needed based on weather conditions. Inspect leaves frequently for any signs of disease.',

    'Orange___Haunglongbing_(Citrus_greening)': 'Use certified disease-free planting material to avoid introducing infections. Regularly monitor trees for insect pests such as psyllids. Implement strict vector control strategies to prevent the spread of disease.',

    'Peach___Bacterial_spot': 'Plant resistant peach varieties in areas prone to bacterial infections. Avoid handling the plants when they are wet to reduce the risk of spreading bacteria. Use copper-based sprays during the early growing stages for added protection.',
    'Peach___healthy': 'Maintain proper pruning and sanitation practices throughout the season. Monitor trees regularly for early signs of bacterial infections. Water at the base to keep leaves dry and reduce disease risks.',

    'Pepper,_bell___Bacterial_spot': 'Plant peppers in raised beds to improve drainage and reduce soil-borne disease pressure. Avoid overcrowding to ensure proper airflow between plants. Sterilize gardening equipment before use to prevent pathogen transfer.',
    'Pepper,_bell___healthy': 'Maintain adequate spacing between plants for good ventilation. Ensure proper soil drainage to avoid waterlogging. Inspect leaves frequently for early symptoms of disease.',

    'Potato___Early_blight': 'Rotate potatoes with non-host crops such as legumes or grains to reduce pathogen buildup. Avoid planting potatoes where tomatoes have grown recently. Remove and destroy infected foliage immediately to limit spread.',
    'Potato___Late_blight': 'Remove volunteer potato plants from fields as they can harbor late blight. Avoid overhead irrigation to reduce leaf wetness and promote drier foliage. Rotate crops each season to prevent disease recurrence.',
    'Potato___healthy': 'Monitor soil drainage to ensure optimal growing conditions. Rotate potato crops every season to reduce the buildup of soil-borne pathogens. Regularly inspect plants for any signs of disease.',

    'Raspberry___healthy': 'Avoid using overhead irrigation to keep leaves dry and reduce fungal growth. Prune old canes regularly to improve airflow and promote new growth. Mulch around the plants to conserve moisture and suppress weeds.',

    'Soybean___healthy': 'Ensure proper planting density to promote airflow and reduce moisture buildup. Monitor fields regularly for pests and diseases. Practice crop rotation to maintain soil health and prevent pathogen accumulation.',

    'Squash___Powdery_mildew': 'Water squash plants at the base to avoid wetting the foliage. Avoid applying excessive nitrogen fertilizers, as lush growth encourages mildew. Remove infected leaves promptly to prevent further spread.',

    'Strawberry___Leaf_scorch': 'Space strawberry plants adequately to improve airflow and reduce disease risks. Remove any infected leaves as soon as they appear. Use mulch to prevent soil splash and maintain clean foliage.',
    'Strawberry___healthy': 'Rotate planting sites to reduce the buildup of soil-borne diseases. Remove weeds around strawberry beds to improve air circulation. Inspect plants regularly for signs of stress or infection.',

    'Tomato___Bacterial_spot': 'Avoid working in tomato fields when plants are wet to prevent spreading bacteria. Sterilize all tools and equipment before use. Rotate crops to reduce soil-borne disease pressure.',
    'Tomato___Early_blight': 'Apply mulch around the base of tomato plants to reduce soil splash onto leaves. Remove lower infected leaves to slow the spread of the disease. Rotate crops yearly to break the pathogen cycle.',
    'Tomato___Late_blight': 'Plant tomatoes in areas with full sun exposure to promote faster leaf drying. Avoid waterlogged soils by improving field drainage. Use resistant varieties whenever available.',
    'Tomato___Leaf_Mold': 'Ensure good ventilation in greenhouses or dense planting areas. Avoid overhead watering to keep leaves dry. Remove infected leaves promptly to limit the spread of mold.',
    'Tomato___Septoria_leaf_spot': 'Avoid overhead watering and use drip irrigation to keep leaves dry. Remove weeds around tomato beds to reduce disease hosts. Mulch the soil surface to limit pathogen splashing.',
    'Tomato___Spider_mites Two-spotted_spider_mite': 'Spray plants with water to dislodge mites and reduce populations. Maintain adequate soil moisture to discourage mite infestations. Keep surrounding areas dust-free, as dust promotes mite outbreaks.',
    'Tomato___Target_Spot': 'Plant disease-resistant tomato varieties where possible. Avoid injuring plants during cultivation or pruning. Rotate crops to prevent the buildup of target spot pathogens in the soil.',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'Use insect-proof nets or row covers to protect plants from whiteflies. Plant virus-free transplants from reliable sources. Monitor and control whitefly populations regularly.',
    'Tomato___Tomato_mosaic_virus': 'Disinfect all tools and hands before handling multiple plants. Avoid smoking or handling tobacco products near tomato plants. Remove and destroy severely infected plants to protect healthy ones.',
    'Tomato___healthy': 'Inspect tomato plants regularly for any changes in leaf color or growth. Maintain balanced fertilization and proper watering practices. Rotate crops yearly to reduce disease risks.',
}
# Default messages in case a label is not found in the dictionary
default_remedy = "Use recommended fungicides and practice good agricultural hygiene."
default_prevention = "Ensure proper spacing, crop rotation, watering practices, and hygiene."
# List of all possible labels for validation