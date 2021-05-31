from django.conf.urls.static import static
from django.urls import path, include

from customer import views
from teont import settings

app_name = 'card'
urlpatterns = [
    path('card/<int:card_id>/', views.view_category.as_view(), name = "card"),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)