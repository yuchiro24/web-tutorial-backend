from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", views.LoginView.as_view()),
    path("retry/", views.RefreshView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("", views.BookView.as_view()),
    path("<int:id>/", views.BookView.as_view()),
]