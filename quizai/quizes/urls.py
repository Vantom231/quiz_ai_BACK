from django.urls import path
from .views import ResoultsView, SubjectSingleView, SubjectView

urlpatterns = [
    path('subject', SubjectView.as_view()),
    path('subject/<int:id>', SubjectSingleView.as_view()),
    path('subject/<int:id>/resoults', ResoultsView.as_view()),
]