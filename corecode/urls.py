from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = "home"),
    
    path('room/<str:values>', views.room, name = "room"),
    
    path('create-room/', views.createRoom, name = "create-room"),
    path('updateUser/',views.updateUser, name='updateUser'),
    
    path('updateRoom/<str:values>',views.updateRoom, name='updateRoom'),
    path('deleteRoom/<str:values>',views.deleteRoom, name='deleteRoom'),
    
    path('deleteMessage/<str:values>',views.deleteMessage, name='deleteMessage'),
    
    path('userlogin/', views.userLogin, name='userlogin'),
    path('userregister/',views.userRegister, name='userregister'),
    path('userlogout/',views.userLogout, name='userlogout'),
    path('userProfile/<str:values>', views.userProfile, name='userProfile'),

    path('topics/',views.topicsView, name='topicsView'),
    path('activities/',views.activity, name='activities'),
]