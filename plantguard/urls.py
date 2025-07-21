"""
URL configuration for plantguard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')

Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Import Django admin site module
from django.contrib import admin

# Import path and include functions for URL routing
from django.urls import path, include

# Import settings and static for serving media files during development
from django.conf import settings
from django.conf.urls.static import static

# Import views from drf_spectacular to generate API schema and docs
from drf_spectacular.views import (
    SpectacularAPIView,        # Generates the OpenAPI schema
    SpectacularRedocView,      # Serves the ReDoc documentation UI
    SpectacularSwaggerView,    # Serves the Swagger UI documentation
)

# Define the URL patterns for the project
urlpatterns = [
    # URL for accessing the Django admin panel
    path('admin/', admin.site.urls),

    # URLs under 'api/account/' are handled by the 'account' app
    path('api/account/', include('account.urls')),

    # URLs under 'api/detection/' are handled by the 'detection' app
    path('api/detection/', include('detection.urls')),

    # URL to get the OpenAPI schema in JSON or YAML format
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # URL to access Swagger UI for API documentation, linked to the schema URL above
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # URL to access ReDoc UI for API documentation (optional alternative to Swagger)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve media files (like uploaded images) during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
