from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from PIL import Image

import customer
from teont import settings
from .forms import PhotoForm
from .models import InfoUser,UserSocial,Social
# Create your views here.
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class Profile(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request):
        user = request.user
        customer, created = InfoUser.objects.get_or_create(user=user)
        social = UserSocial.objects.filter(user=user)
        form = PhotoForm()
        context = {
            'customer':customer,
            'socials': social,
            'form':form,
        }
        return render(request, "customer/customer_profile.html", context);
    def post(self, request):
        username = request.POST['username']


class Social(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request):
        user = User.objects.get(username=request.user.username)
        customer, created = InfoUser.objects.get_or_create(user=user)
        social_customer = user.usersocial_set.all()
        context = {
            'customer': customer,
            'social_customer': social_customer,
        }
        return render(request, "customer/customer_social.html", context);

class ChangePassword(View):
    def get(self,request):
        context = {}
        return render(request, "tapme/change_password.html", context);
    def post(self, request):
        username = request.user.username
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        re_new_password = request.POST['re_new_password']

        user = authenticate(request, username=username, password=old_password)

        # Kiem tra mat khau cu
        if user is None: #mat khau cu sai
            messages.error(request, 'Sai mật khẩu!')
            return render(request, "tapme/change_password.html", {});
        else: #mat khau cu dung
            # Kiem tra 2 mat khau moi
            if new_password != re_new_password:
                messages.error(request, 'Nhập lại mật khẩu mới sai!')
                return render(request, "tapme/change_password.html", {});
            else:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Thay đổi mật khẩu thành công')
                return render(request, "tapme/change_password.html", {});

class ChangeInfoUser(View):
    def get(self, request):
        customer = InfoUser.objects.get(user=request.user)
        context = {'customer': customer}
        return render(request, 'tapme/register.html',context)
    def post(self, request):
        user = request.user
        full_name = request.POST['full_name']
        sub_name = request.POST['sub_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']

        customer, created = InfoUser.objects.get_or_create(user=request.user)
        # Thay doi so dien thoai
        # Kiem tra sdt co trung khong

        if phone_number != InfoUser.objects.get(user=user).phone:
            if InfoUser.objects.filter(phone=phone_number).exists():
                data = {
                    'tag':'error',
                    'title': '',
                    'data': 'Số điện thoại đã tồn tại. Vui lòng chọn số khác!'
                }
                return JsonResponse(data)
            else:
                customer.phone = phone_number

        # # Thay doi email
        # # Kiem tra email co trung khong
        #
        if email != User.objects.get(username=request.user.username).email:
            if User.objects.filter(email=email).exists():
                data = {
                    'tag': 'error',
                    'title': '',
                    'data': 'Email đã tồn tại. Vui lòng chọn email khác!'
                }
                return JsonResponse(data)
            else:
                user.email = email
        # Thay doi sub name
        customer.sub_name = sub_name

        # Thay doi full name
        user.first_name = full_name


        # Luu thay doi
        customer.save()
        user.save()
        # return thanh cong
        data = {
            'tag':'success',
            'title': '',
            'data': 'Thay đổi thông tin thành công'
        }
        return JsonResponse(data)

class ChangeAddress(View):
    def get(self, request):
        return render(request, 'tapme/register.html',{})
    def post(self, request):
        user = request.user
        province = request.POST['province']
        district = request.POST['district']
        commune = request.POST['commune']

        customer, created = InfoUser.objects.get_or_create(user=request.user)
        customer.province = province
        customer.district = district
        customer.commune = commune

        customer.save()
        data = {
            'tag':'success',
            'data': 'Thay đổi địa chỉ thành công'
        }
        return JsonResponse(data)

class ChangeAvatar(View):
    def post(self, request):
        # Thay doi anh dai dien
        if "user_avatar" in request.FILES:
            customer = InfoUser.objects.get(user=request.user)
            social = UserSocial.objects.filter(user=request.user)
            # Lấy file từ request
            myfile = request.FILES["user_avatar"]

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)

            uploaded_file_url = fs.path(filename)


            x = float(request.POST["x"])
            y = float(request.POST["y"])
            w = float(request.POST["width"])
            h = float(request.POST["height"])

            image = Image.open(uploaded_file_url)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((720, 720), Image.ANTIALIAS)
            resized_image.save(uploaded_file_url)
            customer.avatar.delete();
            customer.avatar =  uploaded_file_url
            customer.save();
            return redirect('tapme:customer:customer_profile')
        else:
            return redirect('tapme:page_404')
