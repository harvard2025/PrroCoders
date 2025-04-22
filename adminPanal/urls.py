from django.urls import path
from . import views
urlpatterns = [
    path('', views.adminPanal, name='adminPanal'),
    path('tasks', views.Tasks, name='Tasks'),
    path('Dtasks', views.DTasks, name='DTasks'),
    path('Cobons', views.Cobons, name='Cobons'),
    path('tasks/<int:id>', views.OTask, name='Task'),
    path('Done/<int:id>', views.DoneTasks, name='Done'),
    path('DoneCobons/<int:id>', views.DoneCobons, name='DoneC'),
    path('addCobon/', views.addCobon, name='addCobon'),
    path('addStuff/', views.addEmp, name='Emp'),


]