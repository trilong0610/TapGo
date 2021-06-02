from django.shortcuts import render

# Create your views here.
from django.views import View

from customer.models import *


class ViewCard(View):
    def get(self, request):
        customer = InfoUser.objects.get(user=request.user)
        user = User.objects.get(username=request.user.username)
        userSocial = user.usersocial_set.all()
        context = {
            'customer':customer,
            'userSocial': userSocial
        }
        return render(request,"go/info.html",context)
