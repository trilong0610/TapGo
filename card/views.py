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
    def get(self, request,card_id):
        card = Card.objects.get(id=card_id)
        user = card.user
        customer = InfoUser.objects.get(user=user)
        user_social = card.user.usersocial_set.all()
        context = {
            "user_socials": user_social,
            'card_id': card_id,
            'user':user,
            'customer':customer
        }
        return render(request,"go/info.html",context)

class DemoApi(View):
    def get(self, request):
        post_data = {'username': 'tr.anhh.18'}
        response = requests.post('https://api.findids.net/api/get-uid-from-username', data=post_data)
        content = response.json()
        print(content)
        return HttpResponse(content["data"])