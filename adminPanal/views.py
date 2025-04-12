from django.shortcuts import render
from .models import Task,Cobon
# Create your views here.

def adminPanal(request):
    return render(request, 'adminPanal/index.html')
    


def Tasks(request):
    conText = {
        'Tasks': Task.objects.filter(Done=False).order_by('Date')
    }
    return render(request, 'adminPanal/tasks.html', conText)

def OTask(request, id):
    task = Task.objects.get(pk=id)
    return render(request, 'adminPanal/task.html', {
        'Task':task,
    })

def DoneTasks(request, id):
    task = Task.objects.get(pk=id)
    task.Done = True
    task.save()
    conText = {
        'Tasks': Task.objects.filter(Done=False).order_by('Date')
    }
    return render(request, 'adminPanal/tasks.html', conText)


def Cobons(request):
    conText = {
        'Cobons': Cobon.objects.filter(active=True)
    }
    return render(request, 'adminPanal/cobon.html', conText)



def DoneCobons(request, id):
    cobon = Cobon.objects.get(pk=id)
    cobon.active = False
    cobon.save() 
    conText = {
        'Cobons': Cobon.objects.filter(active=True) 
    }
    return render(request, 'adminPanal/cobon.html', conText)
 