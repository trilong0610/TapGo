from django.conf.urls.static import static
from django.urls import path, include

import tapme
from customer import views
from teont import settings

app_name = 'customer'
urlpatterns = [
    path('profile/', views.Profile.as_view(),name='customer_profile'),
    path('social/', views.Social.as_view(),name='customer_social'),
    path('change-password/', views.ChangePassword.as_view(),name='change_password'),
    path('change_info/', views.ChangeInfoUser.as_view(), name='change_info'),
    path('change_address/', views.ChangeAddress.as_view(), name='change_address'),
    path('change_avatar/', views.ChangeAvatar.as_view(), name='change_avatar'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)