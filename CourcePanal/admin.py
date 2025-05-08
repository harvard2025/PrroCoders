from django.contrib import admin
from .models import Cource, Lesson, Subscribe,Exam,Q, lang, Done_Lessons, Certificate
# Register your models here.

admin.site.register(Cource)
admin.site.register(Lesson)
admin.site.register(Subscribe)
admin.site.register(Exam)
admin.site.register(Q)
admin.site.register(Done_Lessons)
admin.site.register(lang)
admin.site.register(Certificate)




admin.site.site_header = 'PrroCoders'