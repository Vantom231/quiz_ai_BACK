from django.urls import path
from .views import HistoryQuestionView, HistoryQuizView, HistoryQuizViewSingle

urlpatterns = [
    path('quiz/<int:id>/questions', HistoryQuestionView.as_view()),
    path('quiz', HistoryQuizView.as_view()),
    path('quiz/<int:id>', HistoryQuizViewSingle.as_view()),
]