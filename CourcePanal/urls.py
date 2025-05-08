from django.urls import path
from . import views
urlpatterns = [
    path('', views.Cource_view, name='Cource'),
    path('info/<int:id>', views.One_Cource, name='oneCource'),
    path('Sub/<int:id>', views.sub, name='sub'),
    path('UnSub/<int:id>', views.unsub, name='unsub'),
    path('make_subscribe/<int:id>', views.make_sub, name='make_sub'),
    path('Lesson/<int:id>', views.lesson, name='lesson'),
    path('Exam/<int:id>', views.Exam_view, name='Exam'),
    path('submit_test/<int:id>', views.submit_Test, name='submit_test'),
    path('Active/<int:id>', views.Active, name='Active'),
    path('add_Lesson/<int:id>', views.add_Lesson1, name='Add_Lesson'),
    path('create_Lesson/<int:id>', views.create_Lessson, name='Create_Lesson'),
    path('deleat_Lesson/<int:id>', views.deleat_Lesson, name='Deleat_Lesson'),
    path('add_exam/<int:id>', views.add_exam, name='Add_Exam'),
    path('Deleat_exam/<int:id>', views.dealet_exam, name='Deleat_Exam'),
    path('Add_Question/<int:id>', views.Q_V, name='Q'),
    path('Create_Question/<int:id>', views.Create_Q, name='Create_Q'),
    path('Add_Cource/', views.add_Cource, name='Add_Cource'),
    # In CourcePanal/urls.py
    path('course_payment/<int:id>', views.course_payment, name='course_payment'),
    path('course_checkout/<int:id>', views.course_checkout, name='course_checkout'),
    path('payment_success_course/', views.payment_success_course, name='payment_success_course'),
    path('payment_cancel_course/', views.payment_cancel_course, name='payment_cancel_course'),

















]