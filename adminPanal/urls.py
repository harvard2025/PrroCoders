from django.urls import path
from . import views

urlpatterns = [
    # Your existing URLs
    path('', views.adminPanal, name='adminPanal'),
    path('tasks', views.Tasks, name='Tasks'),
    path('Dtasks', views.DTasks, name='DTasks'),
    path('Cobons', views.Cobons, name='Cobons'),
    path('tasks/<int:id>', views.OTask, name='Task'),
    path('Done/<int:id>', views.DoneTasks, name='Done'),
    path('DoneCobons/<int:id>', views.DoneCobons, name='DoneC'),
    path('addCobon/', views.addCobon, name='addCobon'),
    
    # New employee management URLs
    path('employees/', views.employees_list, name='employees_list'),
    path('employees/<int:id>/', views.employee_detail, name='employee_detail'),
    path('addEmployee/', views.addEmp, name='addEmployee'),
    path('editEmployee/<int:id>/', views.editEmp, name='editEmployee'),
    path('terminateEmployee/<int:id>/', views.terminateEmp, name='terminateEmployee'),
    
    # Job management URLs
    path('del_job/<int:id>', views.del_jobs, name='del_jobs'),
    path('Employee/', views.addEmp, name='Emp'),
    path('HR/', views.addHR, name='HR'),

    path('addJob/', views.addJob, name='addJob'),
]