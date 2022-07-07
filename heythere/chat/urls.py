from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('chat-home/', views.chathome , name='chat-home'),
    path('room/<str:room>/', views.room, name='room'),
    path('checkview/', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]