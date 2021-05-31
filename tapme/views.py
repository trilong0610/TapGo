from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.http import request
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from card.models import Card
from customer.models import InfoUser


class Index(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('tapme:customer:customer_profile')
        return render(request, "tapme/login.html",{});

class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('tapme:customer:customer_profile')
        context = {}
        return render(request, "tapme/login.html", context);
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('tapme:customer:customer_profile')
        else:
            messages.error(request, 'Sai tài khoản hoặc mật khẩu!')
            return render(request, "tapme/login.html", {});



class ChangeInfoUser(View):
    def post(self, request):
        username = request.POST['username']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']

        user = authenticate(request, username=username, password=old_password)

        if user is not None:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('tapme:customer:customer_profile')
        else:
            messages.error(request, 'Sai tài khoản hoặc mật khẩu!')
            return render(request, "tapme/login.html", {});

class Register(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('tapme:customer:customer_profile')
        return render(request, "tapme/register.html",{});
    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        card_id = request.POST["card_id"]
        password1 = request.POST["password"]
        password2 = request.POST["repeat_password"]
#         -------Kiem tra user, sdt, email, card code da ton tai chua------
        if is_username_exist(username):
            messages.info(request, 'Tài khoản đã tồn tại!')
            return render(request, "tapme/register.html", {});
        else:
            # --------Kiem tra email ton tai chua-------
            if is_email_exist(email):
                messages.info(request, 'Email đã tồn tại!')
                return render(request, "tapme/register.html", {});
            else:
                # --------Kiem tra card da lien ket voi user nao chua-------
                if is_empty_card_id(card_id) == False:
                    messages.info(request, 'Sai mã thẻ, vui lòng kiểm tra lại!')
                    return render(request, "tapme/register.html", {});
                else:
    #                -----------Dang ky tai khoan----------------
                    if password1 == password2 and password1 != '' and password2 != '':
                        user = User.objects.create_user(username=username, email=email, password=password2)
                        messages.success(request, 'Tạo tài khoản thành công')
                    #     ------Cap nhat lai card-------
                        card = Card.objects.get(id=int(card_id))
                        card.user = User.objects.get(username=username)
                        card.save()
                    # -----------Tao info user-----
                        InfoUser.objects.create(user=user, avatar=settings.MEDIA_ROOT+'/avatars/avatar5.jpeg')
                    else:
                        messages.error(request, 'Vui lòng kiểm tra lại mật khẩu!')
                    return render(request, "tapme/register.html",{});

class ResetPassword(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('tapme:customer:customer_profile')
        return render(request, "tapme/forgotpass.html",{});

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('tapme:index')

def is_email_exist(email):
    if User.objects.filter(email=email).exists():
        return True;
    else:
        return False

def is_username_exist(username):
    if User.objects.filter(username=username).exists():
        return True;
    else:
        return False

def is_empty_card_id(id):
    card = Card.objects.get(id=id)
    if card.user == None:
        return True
    else:
        return False