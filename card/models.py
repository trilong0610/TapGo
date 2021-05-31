from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Card(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.id)
