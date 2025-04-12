from django.urls import path, include
from . import views
urlpatterns = [
    path('Login', views.login_view, name='Login'),
    path('register', views.register, name='register'),
    path("logout", views.logout_view, name="logout"),
]
