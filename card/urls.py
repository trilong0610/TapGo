from django.conf.urls.static import static
from django.urls import path, include

from card import views
from teont import settings

app_name = 'card'
urlpatterns = [
    path('card/<int:card_id>/', views.ViewCard.as_view(), name = "view_card"),
    path('', views.ViewCard.as_view(), name = "view_card"),
    path('demo/', views.DemoApi.as_view(), name = "demo"),


]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)