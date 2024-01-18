from django.conf.urls.static import static
from django.urls import path

from SKIClient import settings
from SKIClient.views import *


urlpatterns = [
    path('', home),
    path('send/', send),
    path('retrieve/', retrieve),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
