
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
import string
from adminPanal.models import Task, Cobon
# Create a simple Task model for this implementation

# A simple store for tasks (in a real app this would be a database)


def WebMakerIndex(request):
    return render(request, 'WebMakerT/index.html')

# @login_required(login_url='Login')
# def Send_Form(request):
#     if request.method == 'POST':
#         # Extract form data
#         name = request.POST.get('name')
#         desc = request.POST.get('desc')
#         idea = request.POST.get('idea')
#         email = request.POST.get('email')
#         number = request.POST.get('number')
        
#         # Check for optional features
#         domain = 'domain' in request.POST
#         dynamic = 'dynamic' in request.POST
#         db = 'db' in request.POST
        
#         # Validate required fields
#         if not all([name, desc, idea, email, number]):
#             messages.error(request, "Please fill in all required fields.")
#             return redirect('WebMakerIndex')
        
#         # Calculate price
#         base_price = 3  # Base cost for website
#         domain_price = 30 if domain else 0
#         dynamic_price = 3 if dynamic else 0
#         db_price = 1 if db and dynamic else 0
        
#         total_price = base_price + domain_price + dynamic_price + db_price
        
#         # Check if there's a discount cobon
#         discount = 0
#         cobon_code = None
#         if 'isC' in request.POST:
#             cobon_code = request.POST.get('cobon')
            
#             cobons = Cobon.objects.all()
#             for cobon1 in cobons:
                
#                 if cobon1.active == True:
#                     print(f'{cobon1.name} == {cobon_code}')
#                     if cobon_code == cobon1.name:
#                         print(cobon1.Sale)
                        
#                         discount = cobon1.Sale
                        
#         date = datetime.now().strftime("%Y-%m-%d")
#     # name = models.CharField(max_length=255) #
#     # desc = models.CharField(max_length=7000) #
#     # idea = models.CharField(max_length=255)#
#     # email = models.CharField(max_length=600)#
#     # number = models.CharField(max_length=30)#
#     # Domain = models.BooleanField(default=False)#
#     # Dynamic = models.BooleanField(default=False)#
#     # DB = models.BooleanField(default=False)#
#     # cobon = models.CharField(max_length=25)#
#     # price = models.FloatField()
#     # Date = models.CharField(max_length=255)
#     # Done = models.BooleanField(default=False)
#         # Create a task object
#         new_task = Task(name=name, desc=desc, idea=idea, email=email, number=number, Domain=domain, Dynamic=dynamic, DB=db, cobon=cobon_code, price=total_price, Date=date, Done=False).save()

#         discount_amount = total_price * (discount / 100)
#         final_price = total_price - discount_amount

#         context = {
#             'task': new_task,
#             'discount_amount': discount_amount,
#             'final_price': final_price,
#         }
        
#         return render(request, 'WebMakerT/price.html', context)


#     # return redirect('WebMakerIndex')

# # def WebMaker_Price(request):
# #     # Get the task from our "database"
# #     task_id = request.session.get('current_task_id')
# #     if not task_id:
# #         messages.error(request, "No active task found.")
# #         return redirect('WebMakerIndex')
    
# #     # task = next((t for t in tasks if t.task_id == task_id), None)
# #     # if not task:
# #     #     messages.error(request, "Task not found.")
# #     #     return redirect('WebMakerIndex')
    
# #     # Calculate final price after discount
# #     discount_amount = task.total_price * (task.discount / 100)
# #     final_price = task.total_price - discount_amount
    
# #     context = {
# #         'task': task,
# #         'discount_amount': discount_amount,
# #         'final_price': final_price,
# #     }
    
#     # return render(request, 'WebMakerT/price.html', context)






@login_required(login_url='Login')
def Send_Form(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        idea = request.POST.get('idea')
        email = request.POST.get('email')
        number = request.POST.get('number')
        
        # Check for optional features
        domain = 'domain' in request.POST
        dynamic = 'dynamic' in request.POST
        db = 'db' in request.POST
        
        # Validate required fields
        if not all([name, desc, idea, email, number]):
            messages.error(request, "Please fill in all required fields.")
            return redirect('WebMakerIndex')
        
        # Calculate price
        base_price = 3  # Base cost for website
        domain_price = 30 if domain else 0
        dynamic_price = 3 if dynamic else 0
        db_price = 1 if db and dynamic else 0
        
        total_price = base_price + domain_price + dynamic_price + db_price
        
        # Check if there's a discount coupon
        discount = 0
        cobon_code = 0
        if 'isC' in request.POST:
            cobon_code = request.POST.get('cobon')
            
            cobons = Cobon.objects.all()
            for cobon1 in cobons:
                if cobon1.active == True:
                    print(f'{cobon1.name} == {cobon_code}')
                    if cobon_code == cobon1.name:
                        print(cobon1.Sale)
                        # Fix: Use assignment operator instead of comparison
                        discount = cobon1.Sale  # Changed == to =
                        
        date = datetime.now().strftime("%Y-%m-%d")
        
        # Create the task object and save it



        # Calculate discount and final price
        discount_amount = total_price * (discount / 100)
        final_price = total_price - discount_amount

        # Prepare context with the new task and pricing informatio
        # n
        new_task = Task(
            name=name, 
            desc=desc, 
            idea=idea, 
            email=email, 
            number=number, 
            Domain=domain, 
            Dynamic=dynamic, 
            DB=db, 
            cobon=cobon_code, 
            price=final_price, 
            Date=date, 
            Done=False
        )
        new_task.save()
        # context = {
        #     'task': new_task,
        #     'total_price': total_price,
        #     'discount': discount,
        #     'discount_amount': discount_amount,
        #     'final_price': final_price,
        # }
        
        # return render(request, 'WebMakerT/price.html', context)
    

        redirect_url = reverse('price') + f'?task_id={new_task.id}&total_price={total_price}&discound={discount}&discound_amount={discount_amount}&final_price={final_price}'
        return HttpResponseRedirect(redirect_url)
    


def price(request):
    task_id = request.GET.get('task_id')
    task = Task.objects.get(id=task_id)  # استرجاع الكائن من الـ ID
    
    total_price = request.GET.get('total_price')
    discound = request.GET.get('discound')
    discound_amount = request.GET.get('discound_amount')
    final_price = request.GET.get('final_price')
    
    context = {
        'task': task,
        'total_price': total_price,
        'discount': discound,
        'discount_amount': discound_amount,
        'final_price': final_price,
    }
    
    return render(request, 'WebMakerT/price.html', context)