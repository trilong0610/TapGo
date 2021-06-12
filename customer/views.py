from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from PIL import Image

import validators
from pip._vendor import requests

import customer
from social.models import Social
from teont import settings
from .forms import PhotoForm
from .models import InfoUser,UserSocial
# Create your views here.
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class ViewProfile(LoginRequiredMixin,View):
    login_url = 'tapme//login/'
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

class ViewSocial(LoginRequiredMixin,View):
    login_url = 'tapme//login/'
    def get(self,request):
        user = User.objects.get(username=request.user.username)
        customer, created = InfoUser.objects.get_or_create(user=user)
        social_customer = user.usersocial_set.all().order_by('social__id')

        # Lấy danh sách id những social đã liên kết của user hiện tại
        list_id_social_customer = user.usersocial_set.all().values_list('social__id', flat=True)

        # Lọc ra những social chưa liên kết với user, tránh liên kết trùng lặp 1 social 2 lần
        socials = Social.objects.exclude(id__in=list_id_social_customer)

        context = {
            'customer': customer,
            'social_customer': social_customer,
            'socials':socials
        }
        return render(request, "customer/customer_social.html", context);

class ChangePassword(LoginRequiredMixin,View):
    login_url = 'tapme/login/'
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

class ChangeInfoUser(LoginRequiredMixin,View):
    login_url = 'tapme/login/'
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

class ChangeAddress(LoginRequiredMixin,View):
    login_url = 'tapme/login/'
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

class ChangeAvatar(LoginRequiredMixin,View):
    login_url = 'tapme/login/'
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
            customer.avatar =  uploaded_file_url.split("media/")[1]
            customer.save();
            return redirect('tapme:customer:customer_profile')
        else:
            return redirect('tapme:page_404')

class AddSocial(LoginRequiredMixin,View):
    login_url = 'tapme/login/'
    def post(self, request):
        user = User.objects.get(username=request.user.username)
        url_social = request.POST["social_url"]
        social_id = int(request.POST["social_id"])
        social = Social.objects.get(id=social_id)
        url_scheme = getSchemeUrl(social_id, url_social)

        if social_id == 7:
            url_social = str(url_social)
            user_social = UserSocial.objects.create(user=request.user, social=social,url_social=url_social, url_scheme=url_scheme)
            # Lưu thành công
            if user_social:
                user_social.save()
                context = {
                    "tag": "success",
                    "data": "Thêm mạng xã hội thành công"
                }
                return JsonResponse(context)

            # Lưu thất bại
            else:
                context = {
                    "tag": "error",
                    "data": "Không tìm thấy mạng xã hội"
                }
                return JsonResponse(context)

        if social_id == 2:
            url_social = str(url_social)

            # Kiem tra do dai neu url la so dien thoai
            if len(url_social) != 10:
                context = {
                    'tag':'error',
                    'data': 'Vui lòng nhập đúng số điện thoại'
                }
                return JsonResponse(context)
            else:
                #     Tìm thấy social
                if social:

                    user_social = UserSocial.objects.create(user=request.user, social=social,url_social=url_social, url_scheme=url_scheme)

                    # Lưu thành công
                    if user_social:
                        user_social.save()
                        context = {
                            "tag": "success",
                            "data": "Thêm mạng xã hội thành công"
                        }
                        return JsonResponse(context)

                    # Lưu thất bại
                    else:
                        context = {
                            "tag": "error",
                            "data": "Không tìm thấy mạng xã hội"
                        }
                        return JsonResponse(context)

                #     không tìm thấy social hoặc url không đúng format
                else:
                    context = {
                        "tag": "error",
                        "data": "Không tìm thấy mạng xã hội"
                    }
                    return JsonResponse(context)

        else:
            if social_id == 3 or social_id == 4 or social_id == 5:
                user_social = UserSocial.objects.create(user=request.user, social=social, url_social=url_social,
                                                        url_scheme=url_scheme)
                # Lưu thành công
                if user_social:
                    user_social.save()
                    context = {
                        "tag": "success",
                        "data": "Thêm mạng xã hội thành công"
                    }
                    return JsonResponse(context)

                # Lưu thất bại
                else:
                    context = {
                        "tag": "error",
                        "data": "Không tìm thấy mạng xã hội"
                    }
                    return JsonResponse(context)
            else:
                #     Tìm thấy social và url đúng format
                if social and validators.url(url_social):

                    user_social = UserSocial.objects.create(user=request.user, social=social, url_social=url_social, url_scheme=url_scheme)

                    # Lưu thành công
                    if user_social:
                        user_social.save()
                        context = {
                            "tag": "success",
                            "data": "Thêm mạng xã hội thành công"
                        }
                        return JsonResponse(context)

                    # Lưu thất bại
                    else:
                        context = {
                            "tag": "error",
                            "data": "Không tìm thấy mạng xã hội"
                        }
                        return JsonResponse(context)

                #     không tìm thấy social hoặc url không đúng format
                else:
                    context = {
                        "tag": "error",
                        "data": "Định dạng liên kết không đúng"
                    }
                    return JsonResponse(context)

class ChangeSocial(LoginRequiredMixin,View):
    login_url = 'tapme/login/'
    def post(self, request):
        url_social = request.POST["social_url"]
        social_id = int(request.POST["social_id"])
        social = Social.objects.get(id=social_id)

        user_social = UserSocial.objects.get(user=request.user, social_id=social_id)

        if social_id == 2 or social_id == 4 or social_id == 10: # Những social dùng số điện thoại

            #     Tìm thấy social
            if user_social :
                user_social.url_social = url_social
                # Lưu thành công
                user_social.save()
                context = {
                    "tag": "success",
                    "data": "Cập nhật thành công"
                }
                return JsonResponse(context)
                # Lưu thất bại
            #     không tìm thấy social hoặc url không đúng format
            else:
                context = {
                    "tag": "error",
                    "data": "Không tìm thấy mạng xã hội"
                }
                return JsonResponse(context)

        else:
            #     Tìm thấy social và url đúng format
            if user_social and validators.url(url_social):
                user_social.url_social = url_social
                # Lưu thành công
                user_social.save()
                context = {
                    "tag": "success",
                    "data": "Cập nhật thành công"
                }
                return JsonResponse(context)

            #     không tìm thấy social hoặc url không đúng format
            else:
                context = {
                    "tag": "error",
                    "data": "Định dạng liên kết không đúng"
                }
                return JsonResponse(context)

class DeleteSocial(LoginRequiredMixin,View):
    login_url = 'tapme/login/'
    def post(self, request):
        social_id = int(request.POST["social_id"])

        user_social = UserSocial.objects.get(user=request.user, social_id=social_id)

        #     Tìm thấy social
        if user_social:
            # Lưu thành công
            user_social.delete()
            context = {
                "tag": "success",
                "data": "Xoá thành công thành công"
            }
            return JsonResponse(context)
            # Lưu thất bại
        #     không tìm thấy social hoặc url không đúng format
        else:
            context = {
                "tag": "error",
                "data": "Xoá thất bại"
            }
            return JsonResponse(context)

class Demo(View):
    def post(self, request):
        social_id = request.POST["social_id"]
        social_user = UserSocial.objects.get(user=request.user, social__id=1)

        # username = ConvertURLToUsername(social_user.social_id,"https://www.facebook.com/teooo.nt/")
        context = {
            'tag':'success',
            # 'data': username
        }
        return JsonResponse(context)

def getSchemeUrl(social_id,url):
    social_id = int(social_id)
    username = ''

    # neu url la so dien thoai thi khong can convert sang username
    if social_id == 2 or social_id == 3 or social_id == 4 or social_id == 5 or social_id == 7 or social_id == 8:
        username = url
    else:
        if url.__contains__('='):
            list = str(url).split('=')
            username = list[len(list) - 1]
        else:
            list = str(url).split('/')
            username = list[len(list)-1]
            if username == '':
                username = list[len(list) - 2]

    if social_id == 1: # FB
        return "fb://profile/" + getUidFacebook(username)
    if social_id == 2: # zalo
        return "https://zalo.me/" + username
    if social_id == 3: # tiktok
        return "snssdk1233://user/profile/" + username
    if social_id == 4: # insta
        return "instagram://user?username=" + username
    if social_id == 5: # email
        return "mailto:" + username
    if social_id == 6: # twi
        return "twitter://user?screen_name=" + username
    if social_id == 7: # tele
        return "tg://resolve?domain=" + username
    if social_id == 8: # bloger
        return username
    if social_id == 9: # linkedin
        return "linkedin://in/" + username

def getUidFacebook(username):
    post_data = {'username': username}
    response = requests.post('https://api.findids.net/api/get-uid-from-username', data=post_data)
    content = response.json()
    return content["data"]["id"]
