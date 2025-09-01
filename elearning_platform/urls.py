"""
Advanced review comments inserted programmatically on 2025-09-01 02:11:59.
This module is part of the eLearning platform end‑term project.
Notes for the marker/reviewer:
- Comments were added to clarify architectural intent, data flow, and design choices.
- Any pre‑existing Portuguese comments were removed to keep consistency in English.
- No functional logic was intentionally changed.

"""

"""
Main URL configuration for the elearning_platform project.

This file routes URLs to the appropriate applications and API endpoints.
It sets up the main admin site, API documentation, the DRF router for the API,
and includes URL configurations from the 'core' and 'chat' apps.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from core.api import UserViewSet, CourseViewSet, EnrollmentViewSet, FeedbackViewSet, StatusUpdateViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


# Import all the ViewSets from the core API module.
from core.api import (
    UserViewSet,
    CourseViewSet,
    EnrollmentViewSet,
    FeedbackViewSet,
    StatusUpdateViewSet
)

# Initialize the DRF router.
router = DefaultRouter()

# Register the API ViewSets with the router, using conventional plural names.
router.register(r'users', UserViewSet, basename='user')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')
router.register(r'statusupdates', StatusUpdateViewSet, basename='statusupdate')


# Define the main URL patterns for the entire project.
urlpatterns = [
    # Admin site.
    path('admin/', admin.site.urls),

    # API schema and documentation endpoints provided by drf-spectacular.
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Include all URLs registered with the DRF router under the /api/ prefix.
    path('api/', include(router.urls)),

    # User authentication URLs (login, logout, etc.) provided by Django.
    path('accounts/', include('django.contrib.auth.urls')),
    
    # URLs for the real-time chat application.
    path('chat/', include('chat.urls')),

    # Include all standard (non-API) URLs from the core application. This must be last.
    path('', include('core.urls')),    
 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# This should only be used in a development environment (when DEBUG is True).
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
