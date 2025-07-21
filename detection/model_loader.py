import os
import tensorflow as tf

# Define model path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'cnn_model', 'plant_disease_prediction_model.h5')

# Global variable to cache the model
_model = None


def get_model():
    """Load and return the trained model (only once)."""
    global _model
    if _model is None:
        _model = tf.keras.models.load_model(model_path)
    return _model
