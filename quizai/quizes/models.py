from django.db import models
from users.models import User


class Subject(models.Model):
    name = models.TextField(255)
    level = models.IntegerField()
    difficulty = models.IntegerField()
    number_finished = models.IntegerField(default=0, blank=True)
    number_of_questions = models.IntegerField(default=5)
    level_class = models.IntegerField(blank=True, null=True)
    question = models.TextField(255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    


class Resoults(models.Model):
    accuracy = models.IntegerField()
    questions_quantity = models.IntegerField()
    creation_date = models.DateTimeField(null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank= True)
