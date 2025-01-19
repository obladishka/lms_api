from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("users/new", UserCreateAPIView.as_view(), name="create_user"),
    path("users/<int:pk>/update", UserUpdateAPIView.as_view(), name="update_user"),
]
