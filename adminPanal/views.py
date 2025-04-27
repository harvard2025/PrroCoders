from django.shortcuts import render, redirect
from .models import Task,Cobon
from datetime import datetime
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

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
    



# Add these imports at the top of views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Cobon, Employee, Jobs
from datetime import datetime
from django.contrib import messages
from django.db.models import Q

# Your existing views here...

# Employee Management Views
def employees_list(request):
    """View all employees with optional filtering"""
    # Default queryset
    employees = Employee.objects.filter(active=True)
    
    # Handle search and filters
    search_query = request.GET.get('search', '')
    job_filter = request.GET.get('job', '')
    sort_by = request.GET.get('sort', 'First_name')
    
    if search_query:
        employees = employees.filter(
            Q(First_name__icontains=search_query) | 
            Q(Last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if job_filter:
        employees = employees.filter(job=job_filter)
    
    # Apply sorting
    employees = employees.order_by(sort_by)
    
    # Get all job titles for the filter dropdown
    jobs = Jobs.objects.all()
    
    context = {
        'employees': employees,
        'jobs': jobs,
        'search_query': search_query,
        'job_filter': job_filter,
        'sort_by': sort_by
    }
    return render(request, 'adminPanal/employees_list.html', context)

def employee_detail(request, id):
    """View details of a specific employee"""
    employee = get_object_or_404(Employee, pk=id)
    return render(request, 'adminPanal/employee_detail.html', {'employee': employee})

def addEmp(request):
    """Add a new employee"""
    if request.method == "POST":
        # Get form data
        first_name = request.POST.get('Fname')
        last_name = request.POST.get('Lname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('conpassword')
        salary = request.POST.get('salary')
        about = request.POST.get('about')
        email = request.POST.get('email')
        number = request.POST.get('number')
        job = request.POST.get('job')
        portfolio = request.POST.get('portfolio')
        
        # Validate passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'adminPanal/add_employee.html', {
                'jobs': Jobs.objects.all(),
                'message': "Passwords do not match!"
            })
        
        # Get current date for start date
        current_year = int(datetime.now().strftime("%Y"))
        current_month = int(datetime.now().strftime("%m"))
        current_day = int(datetime.now().strftime("%d"))
        
        # Handle file upload for CV
        cv_file = request.FILES.get('cv', None)
        
        # Create the employee
        new_employee = Employee(
            First_name=first_name,
            Last_name=last_name,
            user_name=username,
            password=password,  # Note: In production, password should be hashed
            salary=salary,
            about=about,
            email=email,
            number=number,
            job=job,
            prto=portfolio,
            Syear=current_year,
            Smonth=current_month,
            Sday=current_day,
            # End date defaults to the same as start date
            Eyear=current_year  ,
            Emonth=current_month,
            Eday=current_day,
            active=True
        )
        user = User.objects.create_user(username = username, email = email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = False
        user.save()
        if cv_file:
            new_employee.cv = cv_file
            
        new_employee.save()
        messages.success(request, f"Employee {first_name} {last_name} added successfully!")
        return redirect('employees_list')
    else:
        jobs = Jobs.objects.all()
        return render(request, 'adminPanal/add_employee.html', {'jobs': jobs})

def editEmp(request, id):
    """Edit an existing employee"""
    employee = get_object_or_404(Employee, pk=id)
    
    if request.method == "POST":
        # Update employee details
        employee.First_name = request.POST.get('Fname')
        employee.Last_name = request.POST.get('Lname')
        employee.user_name = request.POST.get('username')
        employee.salary = request.POST.get('salary')
        employee.about = request.POST.get('about')
        employee.email = request.POST.get('email')
        employee.number = request.POST.get('number')
        employee.job = request.POST.get('job')
        employee.prto = request.POST.get('portfolio')
        
        # Check if a new password was provided
        new_password = request.POST.get('password')
        if new_password:
            confirm_password = request.POST.get('conpassword')
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return render(request, 'adminPanal/edit_employee.html', {
                    'employee': employee,
                    'jobs': Jobs.objects.all(),
                    'message': "Passwords do not match!"
                })
            employee.password = new_password  # Should be hashed in production
        
        # Handle CV update if provided
        if 'cv' in request.FILES:
            employee.cv = request.FILES['cv']
        
        employee.save()
        messages.success(request, f"Employee {employee.First_name} {employee.Last_name} updated successfully!")
        return redirect('employees_list')
        
    jobs = Jobs.objects.all()
    return render(request, 'adminPanal/edit_employee.html', {
        'employee': employee,
        'jobs': jobs
    })

def terminateEmp(request, id):
    """Terminate/deactivate an employee"""
    employee = get_object_or_404(Employee, pk=id)
    userE = User.objects.get(username = employee.user_name)
    userE.is_active = False
    userE.save()
    
    if request.method == "POST":
        # Update end date to current date
        employee.Eyear = int(datetime.now().strftime("%Y"))
        employee.Emonth = int(datetime.now().strftime("%m"))
        employee.Eday = int(datetime.now().strftime("%d"))
        employee.active = False
        employee.save()
        
        messages.success(request, f"Employee {employee.First_name} {employee.Last_name} has been terminated.")
        return redirect('employees_list')
        
    return render(request, 'adminPanal/terminate_employee.html', {'employee': employee})

def addJob(request):
    """Add a new job title"""
    if request.method == "POST":
        job_name = request.POST.get('job_name')
        if job_name:
            Jobs.objects.create(name=job_name)
            messages.success(request, f"Job '{job_name}' added successfully!")
        return redirect('addJob')
    
    jobs = Jobs.objects.all()
    return render(request, 'adminPanal/add_job.html', {'jobs': jobs})

def del_jobs(request, id):
    job = Jobs.objects.get(pk=id)
    job.delete()
    return redirect('addJob')





def addHR(request):
    """Add a new HR"""
    if request.method == "POST":
        # Get form data
        first_name = request.POST.get('Fname')
        last_name = request.POST.get('Lname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('conpassword')
        salary = request.POST.get('salary')
        about = request.POST.get('about')
        email = request.POST.get('email')
        number = request.POST.get('number')
        job = request.POST.get('job')
        portfolio = request.POST['portfolio']
        
        # Validate passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'adminPanal/HR.html', {
                'jobs': Jobs.objects.all(),
                'message': "Passwords do not match!"
            })
        
        # Get current date for start date
        current_year = int(datetime.now().strftime("%Y"))
        current_month = int(datetime.now().strftime("%m"))
        current_day = int(datetime.now().strftime("%d"))
        
        # Handle file upload for CV
        cv_file = request.FILES.get('cv', None)


        
        # Create the employee
        new_employee = Employee(
            First_name=first_name,
            Last_name=last_name,
            user_name=username,
            password=password,  # Note: In production, password should be hashed
            salary=salary,
            about=about,
            email=email,
            number=number,
            job=job,
            prto=portfolio,
            Syear=current_year,
            Smonth=current_month,
            Sday=current_day,
            # End date defaults to the same as start date
            Eyear=current_year  ,
            Emonth=current_month,
            Eday=current_day,
            active=True
        )
        user = User.objects.create_superuser(username = username, email = email, password=password)
        user.is_superuser =True
        user.save()
        if cv_file:
            new_employee.cv = cv_file
            
        new_employee.save()
        messages.success(request, f"Employee {first_name} {last_name} added successfully!")
        return redirect('employees_list')
    else:
        jobs = Jobs.objects.all()
        return render(request, 'adminPanal/HR.html', {'jobs': jobs})
