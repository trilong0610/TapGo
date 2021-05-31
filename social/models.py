from django.db import models

# Create your models here.
class Social(models.Model):
    id = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length=255, null= True, blank= True)
    img = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def get_all_social(self):
        return Social.objects.all()