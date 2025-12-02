"""
URL configuration for config project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from apps.common.views import SecureMediaView

# Imports for Documentation
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="ProjectR API",
      default_version='v1',
      description="API documentation for ProjectR",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@projectr.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

admin.site.site_header = "ProjectR"

urlpatterns = [
    path('account/', include('apps.account.urls', namespace='account')),
    path('common/', include('apps.common.urls', namespace='common')), # Added Common App URLs
    path('', include('apps.dashboard.urls', namespace='dashboard')),
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', SecureMediaView.as_view(), name='secure_media'),

    # --- API Documentation URLs ---
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)