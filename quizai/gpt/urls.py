from django.urls import path
from .views import generationView

urlpatterns = [
    path('subject/<int:id>/generate', generationView.as_view()),
]