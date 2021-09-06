from django.urls import path
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenRefreshView

from .views import create_user_and_get_token, send_code

urlpatterns = [
    path('api-token-auth/',
         views.obtain_auth_token),
    path('token/',
         create_user_and_get_token,
         name='token_obtain_pair'),
    path('email/',
         send_code),
    path('token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]
