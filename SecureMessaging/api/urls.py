from api import views
from django.urls import path


urlpatterns = [
    path('message/<str:message_id>/', views.get_message),
    path('message/', views.create_message),
]
