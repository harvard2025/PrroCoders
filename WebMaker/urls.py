from django.urls import path
from . import views

urlpatterns = [
    path('', views.WebMakerIndex, name='WebMaker'),
    path('send_form/', views.Send_Form, name='Send_Form'),
    # path('price/', views.WebMaker_Price, name='WebMaker_Price'),
]