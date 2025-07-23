import os
import django
import pandas as pd
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.paginator import Paginator

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plantguard.settings')
django.setup()

from detection.models import PredictionHistory


def is_superuser(username, password):
    user = authenticate(username=username, password=password)
    return user and user.is_superuser


def get_user_metrics():
    total_users = User.objects.count()
    total_predictions = PredictionHistory.objects.count()
    most_predicted = (
        PredictionHistory.objects.values('disease')
        .annotate(count=Count('disease'))
        .order_by('-count')
        .first()
    )
    return {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "most_predicted": most_predicted['disease'] if most_predicted else "N/A"
    }


def get_user_growth():
    users = User.objects.extra({'date': "date(date_joined)"}).values('date').annotate(count=Count('id')).order_by(
        'date')
    df = pd.DataFrame(users)
    return df


def get_predictions_by_disease():
    preds = PredictionHistory.objects.values('disease').annotate(count=Count('id')).order_by('-count')
    df = pd.DataFrame(preds)
    return df


def get_predictions_per_day():
    preds = PredictionHistory.objects.extra({'date': "date(timestamp)"}).values('date').annotate(
        count=Count('id')).order_by('date')
    df = pd.DataFrame(preds)
    return df


def get_users(search=None, is_staff=None, is_superuser=None):
    qs = User.objects.all()
    if search:
        qs = qs.filter(username__icontains=search)
    if is_staff is not None:
        qs = qs.filter(is_staff=is_staff)
    if is_superuser is not None:
        qs = qs.filter(is_superuser=is_superuser)
    return qs


def paginate_queryset(qs, page, per_page):
    paginator = Paginator(qs, per_page)
    return paginator.get_page(page)


def get_predictions(search=None, user=None, disease=None, date=None):
    qs = PredictionHistory.objects.all()
    if search:
        qs = qs.filter(id__icontains=search)
    if user:
        qs = qs.filter(user__username__icontains=user)
    if disease:
        qs = qs.filter(disease__icontains=disease)
    if date:
        qs = qs.filter(timestamp__date=date)
    return qs


def get_history(search=None, user=None, disease=None, date=None):
    # For this project, history is the same as predictions
    return get_predictions(search, user, disease, date)


def save_model_file(uploaded_file):
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(models_dir, exist_ok=True)
    file_path = os.path.join(models_dir, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def list_models():
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    if not os.path.exists(models_dir):
        return []
    files = []
    for fname in os.listdir(models_dir):
        fpath = os.path.join(models_dir, fname)
        if os.path.isfile(fpath):
            files.append({
                "name": fname,
                "path": fpath,
                "upload_date": pd.to_datetime(os.path.getmtime(fpath), unit='s')
            })
    files.sort(key=lambda x: x['upload_date'], reverse=True)
    return files


def set_active_model(model_name):
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    active_path = os.path.join(models_dir, 'active_model.txt')
    with open(active_path, 'w') as f:
        f.write(model_name)


def get_active_model():
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    active_path = os.path.join(models_dir, 'active_model.txt')
    if os.path.exists(active_path):
        with open(active_path, 'r') as f:
            return f.read().strip()
    return None
