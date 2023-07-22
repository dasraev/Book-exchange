from django.urls import path
from .views import room,rooms

urlpatterns = [
    path('rooms/',rooms,name='rooms'),
    path('<email1>/', room, name='chat'),
]

