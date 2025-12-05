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
    path('common/', include('apps.common.urls', namespace='common')),
    path('chat/', include('apps.chat.urls', namespace='chat')), # Added Chat URLs
    path('', include('apps.dashboard.urls', namespace='dashboard')),
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', SecureMediaView.as_view(), name='secure_media'),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)