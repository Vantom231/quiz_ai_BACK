from django.db import models
from users.models import User


class Subject(models.Model):
    name = models.TextField(255)
    level = models.IntegerField()
    difficulty = models.IntegerField()
    number_finished = models.IntegerField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_questions = models.IntegerField(default=5)


class Resoults(models.Model):
    accuracy = models.IntegerField()
    questions_quantity = models.IntegerField()
    creation_date = models.DateTimeField(null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank= True)
