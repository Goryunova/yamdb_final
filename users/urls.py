from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet

v1_router = DefaultRouter(trailing_slash=True)
v1_router.register(r'', UsersViewSet)

urlpatterns = [
    path('', include(v1_router.urls))
]
