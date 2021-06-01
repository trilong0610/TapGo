from django.conf.urls.static import static
from django.urls import path, include

from tapme import views
from teont import settings

app_name = 'tapme'
urlpatterns = [
    path('customer/', include('customer.urls')),
    path('', views.Login.as_view(),name='index'),
    path('login/', views.Login.as_view() ,name='login'),
    path('logout/', views.Logout.as_view(),name='logout'),
    path('register/', views.Register.as_view(),name='register'),
    path('reset-password/', views.ResetPassword.as_view(),name='reset_password'),
    path('404/', views.Page_404.as_view(),name="page_404"),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)