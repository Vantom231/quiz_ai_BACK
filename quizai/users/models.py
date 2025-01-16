from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    subject_created = models.IntegerField(blank=True, default=0)
    generated_quizes = models.IntegerField(blank=True, default=0)
    finished_quizes = models.IntegerField(blank=True, default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
# Create your models here.
