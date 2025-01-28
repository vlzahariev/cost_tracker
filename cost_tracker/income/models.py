from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True, null=True)
    date = models.DateField(null=True, blank=True)
