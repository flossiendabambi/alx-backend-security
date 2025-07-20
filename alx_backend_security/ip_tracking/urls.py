from django.urls import path
from .views import anonymous_sensitive_view, authenticated_sensitive_view

urlpatterns = [
    path('anon-login/', anonymous_sensitive_view, name='anon_login'),
    path('auth-login/', authenticated_sensitive_view, name='auth_login'),
]
