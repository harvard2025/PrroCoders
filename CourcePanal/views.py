from django.shortcuts import render
from django.http import HttpResponseRedirect ,HttpResponse
from .models import Cource, Lesson, Subscribe,Exam,Q,lang, Done_Lessons
from django.contrib.auth.models import AbstractUser, User
from django.urls import reverse
import random
# Create your views here.
def Cource_view(request):
    return render(request, 'Cource/index.html', {
        'Cources':Cource.objects.all()
    })
def One_Cource(request, id):
    OneCource = Cource.objects.get(pk=id)
    isSub = False
    SubscribeUser = None
    DoneLessons = Done_Lessons.objects.filter(User=request.user).values_list('Done_Lesson_id', flat=True)  

    for Sub in OneCource.Subscribe.all():
        if Sub.User == request.user:
            isSub = True
            SubscribeUser = Sub

    return render(request, 'Cource/One_Cource.html', {
        'Cource': OneCource,
        'Lessons': OneCource.Lesson.all(),
        'Subscribe': OneCource.Subscribe.all(),
        'isSub': isSub,
        'Sub': SubscribeUser,
        'DoneLessons': list(DoneLessons),  # قائمة تحتوي على الـ ID فقط لتحسين الأداء
    })


def sub(request, id):
    OneCource = Cource.objects.get(pk=id)
    return render(request, 'Cource/sub.html', {
        'Cource': OneCource,
        'message': 'else'
    })
def unsub(request, id):
        new_sub = Subscribe.objects.get(User=request.user)
        new_sub.delete()
        return HttpResponseRedirect(reverse('oneCource', args=(id,)))

def make_sub(request, id):
    if request.method == 'POST':
        OneCource = Cource.objects.get(pk=id)
        Cer_Name = request.POST['Certificate_Name']
        user = User.objects.get(pk=request.user.id)

        new_sub = Subscribe.objects.create(User=user,Certificate_Name=Cer_Name,Cource=OneCource)
        return HttpResponseRedirect(reverse('oneCource', args=(id,)))
        

# def lesson(request, id):

#     lesson1 = Lesson.objects.get(pk=id)
#     OneCource= lesson1.Cource
#     isSub = False
#     SubscribeUser = None
#     for Sub in OneCource.Subscribe.all():
#         if Sub.User == request.user:
#             isSub = True
#             SubscribeUser = Sub
    
#     return render(request, 'Cource/Lesson.html', {
#         'Lesson':lesson1,
#         'isSub':isSub,
#     })


def lesson(request, id):
    lesson1 = Lesson.objects.get(pk=id)
    isSub = False
    SubscribeUser = None
    for Sub in lesson1.Cource.Subscribe.all():
        if Sub.User == request.user:
            isSub = True
            SubscribeUser = Sub
    exam = Exam.objects.filter(Lesson=lesson1)
    isExam = exam.exists()
    
    # تعديل رابط YouTube إلى صيغة قابلة للتضمين
    lesson_url = lesson1.Url
    if "youtube.com/watch?v=" in lesson_url:
        lesson_url = lesson_url.replace("watch?v=", "embed/")
    elif "youtu.be/" in lesson_url:
        lesson_url = lesson_url.replace("youtu.be/", "youtube.com/embed/")

    return render(request, 'Cource/Lesson.html', {
        'Lesson': lesson1,
        'isSub': isSub,
        'lesson_url': lesson_url,  # إرسال الرابط المعدل للقالب
        'isExam':isExam,
    })




def Exam_view(request, id):
    lesson1 = Lesson.objects.get(pk=id)
    exam = Exam.objects.get(Lesson=lesson1)
    Q_L = []
    Questions = Q.objects.filter(Exam=exam)
    for Question in Questions:
        Q_L.append(Question)

    random.shuffle(Q_L)
    return render(request, 'Cource/Exam.html', {
        'Lesson':lesson1,
        'Exam':exam,
        'Q':Q_L,
    })


def submit_Test(request, id):
    exam = Exam.objects.get(pk=id)
    questions = Q.objects.filter(Exam=exam)
    total_questions = questions.count()  # استخدم دالة count() بدلاً من الخاصية
    score = 0
    
    for question in questions:
        # استخدام get بدلاً من [] للتأكد من عدم حدوث خطأ إذا لم توجد إجابة
        user_answer = request.POST.get(f"answer_{question.id}", "").strip()
        correct_answer = question.TrueAnswer.strip()  # تأكد من أن الحقل TrueAnswer صحيح
        
        if user_answer == correct_answer:
            score += 1  # زيادة الدرجة إذا كانت الإجابة صحيحة

    # حساب النسبة المئوية
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    Succes = None
    if score > (total_questions // 2):
        Succes = True  # اسم المتغير يجب أن يبدأ بحرف صغير حسب PEP8
        
        # احصل على الدرس المرتبط بالامتحان
        lesson = Lesson.objects.get(Exam=exam)

        # احصل على الكورس المرتبط بالدرس
        course = lesson.Cource  

 

        exam.save()
        lesson.save()
        
        Lessons = course.Lesson.all()
        Lessons_num = Lessons.count()

        DL = Done_Lessons.objects.create(User = request.user, Done_Lesson=lesson)
        DL.save()
        Succes = True 
    else:
        Succes = False
    return render(request, 'Cource/Test_Result.html', {
        'exam': exam,
        'score': score,
        'total': total_questions,
        'percentage': percentage,
        'Succes': Succes,
    })

def Active(request, id):
    OneCource = Cource.objects.get(pk=id)
    if OneCource.isActive == True:
        OneCource.isActive = False
        OneCource.save()
    else:
        OneCource.isActive = True
        OneCource.save()
    return HttpResponseRedirect(reverse('oneCource', args=(id,)))

def add_Lesson1(request, id):

    OneCource = Cource.objects.get(pk=id)
    return render(request, 'Cource/add_Lesson.html', {
        'Cource' : OneCource
    })
    
def create_Lessson(request, id):
    if request.method == 'POST':
        OneCource = Cource.objects.get(pk=id)
        url = request.POST.get('url')
        name = request.POST.get('Name')
        des = request.POST.get('description')
        C = OneCource
        L = Lesson.objects.create(Url=url, Name=name, description=des, Cource=C)
        return HttpResponseRedirect(reverse('oneCource', args=(id,)))
def deleat_Lesson(request, id):
    lesson1 = Lesson.objects.get(pk=id)
    lesson1.delete()
    return HttpResponseRedirect(reverse('oneCource', args=(lesson1.Cource.id,)))

def add_exam(request,id):
    lesson1 = Lesson.objects.get(pk=id)
    name = lesson1.Name
    E = Exam.objects.create(Lesson=lesson1, Name=name)
    E.save()
    return HttpResponseRedirect(reverse('lesson', args=(id,)))
    # if request.method == 'POST':
    #     return  
    # else:
    #     return render(request, 'Cource/add_exam.html', {
    #         'Lesson':lesson1,
    #     })


def dealet_exam(request,id):
    E = Exam.objects.get(pk=id)
    E.delete()
    return HttpResponseRedirect(reverse('lesson', args=(E.Lesson.id,)))

def Q_V(request, id):
    return render(request, 'Cource/add_Q.html', {
        'id':id,
    })
def Create_Q(request,id):
    if request.method == 'POST':
        E = Exam.objects.get(pk=id)
        q = request.POST.get('Qe')
        answer11 = request.POST.get('answer1')
        answer21 = request.POST.get('answer2')
        answer31 = request.POST.get('answer3')
        TrueAnswer = request.POST.get('TrueAnswer')
        A = [answer11,answer21,answer31]
        random.shuffle(A)
        answer1 = A[0]
        answer2 = A[1]
        answer3 = A[2]
        Ques = Q.objects.create(Exam=E, Q=q, answer1=answer1, answer2=answer2, answer3=answer3, TrueAnswer=TrueAnswer)
        Ques.save()
        return HttpResponseRedirect(reverse('Exam', args=(E.Lesson.id,)))
    

def add_Cource(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        name = request.POST['Name']
        description = request.POST['description']
        duration = request.POST['duration']
        By = request.POST['By']
        price = request.POST['price']
        lang_name = request.POST['lang']
        try:
            lang_obj = lang.objects.get(name=lang_name)  # البحث باستخدام الاسم
        except lang.DoesNotExist:
            return HttpResponse("Error: Language not found", status=400)
        C = Cource.objects.create(image=image,Name=name,description=description,duration=duration,isActive=True,By=By,price=price,lang=lang_obj)
        C.save()
        return HttpResponseRedirect(reverse('Cource'))

    else:
        return render(request, 'Cource/add_Cource.html',{
            'langs': lang.objects.all()
        })