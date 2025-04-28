from django.urls import path
from . import views
app_name = 'store'
urlpatterns = [
    path('/use_<int:use>', views.index, name='store'),
    # path('Filter', views.Fcat, name='filter')
]