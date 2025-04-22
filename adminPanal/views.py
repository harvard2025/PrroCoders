from django.shortcuts import render, redirect
from .models import Task,Cobon
from datetime import datetime
# Create your views here.

def adminPanal(request):
    return render(request, 'adminPanal/index.html')
    


def Tasks(request):
    conText = {
        'Tasks': Task.objects.filter(Done=False).order_by('Date')
    }
    return render(request, 'adminPanal/tasks.html', conText)

def DTasks(request):
    conText = {
        'Tasks': Task.objects.filter(Done=True).order_by('Date')
    }
    return render(request, 'adminPanal/DoneT.html', conText)


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
    # return render(request, 'adminPanal/cobon.html', conText)
    return redirect('Cobons')
 

def addCobon(request):
    if request.method == "POST":
        name = request.POST['name']
        sale = request.POST['sale']
        #datetime.now().strftime("%Y-%m-%d")
        y = datetime.now().strftime("%Y")
        m =datetime.now().strftime("%m")
        d = datetime.now().strftime("%d")
        newCobon =  Cobon.objects.create(name=name,Sale=sale,Eyear=y,Emonth=m,Eday=d,active=True).save()
        return redirect('Cobons')



def addEmp(request):
    if request.method == "POST":
        pass
    else:
        return render(request, 'adminPanal/Emp.html')