from django.urls import path
from . import views

urlpatterns = [
    path("", views.BookView.as_view()),
    path("<int:id>/", views.BookView.as_view()),
]