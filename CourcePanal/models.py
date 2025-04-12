from django.db import models
from django.contrib.auth.models import AbstractUser, User
# Create your models here.


class lang(models.Model):
    name = models.CharField(max_length=10)

class Cource(models.Model):
    image = models.ImageField(upload_to='courses/', default='default.png')
    Name = models.CharField(max_length=30)
    description = models.CharField(max_length=400)
    duration = models.IntegerField()
    isActive = models.BooleanField(default=True)
    By = models.CharField(max_length=30)
    price = models.IntegerField()
    lang = models.ForeignKey(lang, on_delete=models.CASCADE, related_name='Cource')
    


class Subscribe(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Subscribe')
    Certificate_Name = models.CharField(max_length=255)
    Cource = models.ForeignKey(Cource, on_delete=models.CASCADE, related_name='Subscribe')
    Done_Cource = models.BooleanField(default=False)
    Done_Lesson = models.BooleanField(default=False)
    Done_Exam = models.BooleanField(default=False)



class Lesson(models.Model):
    Url = models.CharField(max_length=300)
    Name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    Cource = models.ForeignKey(Cource, on_delete=models.CASCADE, related_name='Lesson')

class Done_Lessons(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='DoneLessons')
    Done_Lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='DoneLessons')

class Exam(models.Model):
    Lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='Exam')
    Name =models.CharField(max_length=30)

class Q(models.Model):
    Exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='Q')
    Q = models.CharField(max_length=2000)
    answer1 = models.CharField(max_length=2000)
    answer2 = models.CharField(max_length=2000)
    answer3 = models.CharField(max_length=2000)
    TrueAnswer = models.CharField(max_length=2000)




# class Certificate(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Cource, on_delete=models.CASCADE)
#     file = models.FileField(upload_to='certificates/')
#     created_at = models.DateTimeField(auto_now_add=True)
    
class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Cource, on_delete=models.CASCADE, related_name='certificates')
    certificate_file = models.FileField(upload_to='certificates/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.Name}"