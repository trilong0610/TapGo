from django.db import models
from django.contrib.auth.models import User

from card.models import Card
from social.models import Social
# Create your models here.
class InfoUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    sub_name = models.CharField(max_length=255, null=True, blank=True);
    phone = models.CharField(max_length=10, null=True, blank=True);
    province = models.CharField(max_length=255, null=True, blank=True);
    district = models.CharField(max_length=255, null=True, blank=True);
    commune = models.CharField(max_length=255, null=True, blank=True);
    avatar = models.ImageField(default='statics/media/avatars/avatar5.jpeg',null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def avatarURL(self):
        try:
            url = self.avatar.url
        except:
            url = ''
        return url

class UserSocial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    social = models.ForeignKey(Social, on_delete=models.CASCADE,blank=True, null=True)
    url_social = models.CharField(max_length=255,null=True, blank=True)
    url_scheme = models.CharField(max_length=255,null=True, blank=True)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
