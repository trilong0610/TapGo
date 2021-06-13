from django.conf.urls.static import static
from django.urls import path, include

from card import views
from teont import settings

app_name = 'card'
urlpatterns = [


]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)