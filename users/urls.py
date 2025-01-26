from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (PaymentListAPIView, UserCreateAPIView, UserDestroyAPIView, UserListAPIView,
                         UserRetrieveAPIView, UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("users/register", UserCreateAPIView.as_view(), name="create_user"),
    path("users/login", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="user_login"),
    path("users/token/refresh", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="user_token_refresh"),
    path("users", UserListAPIView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("users/<int:pk>/update", UserUpdateAPIView.as_view(), name="update_user"),
    path("users/<int:pk>/delete", UserDestroyAPIView.as_view(), name="delete_user"),
    path("payments", PaymentListAPIView.as_view(), name="payment_list"),
]
