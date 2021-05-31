from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Multimedia(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    music = models.FileField()
    video = models.FileField()

    def __str__(self):
        return self.user