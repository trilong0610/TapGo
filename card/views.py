import json
import urllib
from types import SimpleNamespace

from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views import View
from pip._vendor import requests
import urllib3
from customer.models import *


class ViewCard(View):
    def get(self, request):
        # customer = InfoUser.objects.get(user=request.user)
        # user = User.objects.get(username=request.user.username)
        # userSocial = user.usersocial_set.all()
        context = {

        }
        return render(request,"go/info.html",context)

class DemoApi(View):
    def get(self, request):
        post_data = {'username': 'tr.anhh.18'}
        response = requests.post('https://api.findids.net/api/get-uid-from-username', data=post_data)
        content = response.json()
        print(content)
        return HttpResponse(content["data"])