# 🌿 Plant Disease Detection API

An intelligent, authenticated API for detecting plant diseases from images. Built with **Django REST Framework**, it features user authentication, prediction history tracking, and JWT-based security.

---

## 🧠 App Summary

This app provides:

- ✅ User registration, login, logout, and profile updates
- 🧠 AI-based plant disease detection from uploaded images
- 📜 Prediction history tracking (retrieve, view detail, delete)
- 🔐 JWT authentication (access & refresh tokens with blacklist support)

---

## 🔐 Authentication APIs

| Method | Endpoint                     | Description                                                       |
|--------|------------------------------|-------------------------------------------------------------------|
| POST   | `/api/account/login/`        | Log in user and receive JWT access & refresh tokens               |
| POST   | `/api/account/logout/`       | Logout user by blacklisting the refresh token                     |
| POST   | `/api/account/refresh/`      | Generate new access token using refresh token                     |
| POST   | `/api/account/register/`     | Register a new user                                               |
| PUT    | `/api/account/update_profile/` | Update profile info of the authenticated user                  |
| GET    | `/api/account/user_detail/`  | Fetch profile details of the currently authenticated user         |

---

## 🌱 Plant Disease Detection APIs

| Method | Endpoint                                 | Description                                            |
|--------|------------------------------------------|--------------------------------------------------------|
| POST   | `/api/detection/predict/`                | Upload plant image to receive disease prediction       |
| GET    | `/api/detection/history/`                | View all prediction history for the current user       |
| GET    | `/api/detection/history/{id}/`           | View detailed info about a specific prediction         |
| DELETE | `/api/detection/history/{id}/delete/`    | Delete a specific prediction                          |
| DELETE | `/api/detection/history/clear/`          | Delete all prediction history for the current user     |

---

## 🧑‍💼 Admin APIs (Django Admin Panel)

| Access | URL                        | Description                               |
|--------|----------------------------|-------------------------------------------|
| GET    | `/admin/`                  | Admin login dashboard                     |
| GET    | `/admin/account/user/`     | Manage all registered users               |
| GET    | `/admin/detection/prediction/` | View or delete any prediction history |

> ℹ️ All admin endpoints are accessible via the Django admin panel.  
> Requires login with superuser credentials.

---

## 🧪 Other Endpoints

| Method | Endpoint         | Description                      |
|--------|------------------|----------------------------------|
| GET    | `/api/schema/`   | OpenAPI/Swagger schema for the API |

---

## 📦 Tech Stack

- Python 3.10+
- Django 5.x
- Django REST Framework
- SimpleJWT (for JWT authentication)
- TensorFlow/Keras 

---

## 🚀 How to Use

1. **Clone the repo**  
   ```bash
   git clone https://github.com/pankajrajparajuli/plant-disease-api.git
   cd plant-disease-api
2. **Create virtual environment & install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
3. **Apply migrations & run the server**
   ```bash
   python manage.py migrate
   python manage.py runserver
   
4. ***Access the API docs***
    Visit http://127.0.0.1:8000/api/docs/
