from django.db import models
from users.models import User


class HistoryQuiz(models.Model):
    number = models.IntegerField()
    subject = models.CharField(max_length=255)
    accuracy = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

class HistoryQuestion(models.Model):
    question = models.CharField(max_length=255)
    anw_a = models.CharField(max_length=255)
    anw_b = models.CharField(max_length=255)
    anw_c = models.CharField(max_length=255)
    anw_d = models.CharField(max_length=255)
    anw = models.CharField(max_length=1)
    anw_correct = models.CharField(max_length=1)
    quiz = models.ForeignKey(HistoryQuiz, on_delete=models.CASCADE)