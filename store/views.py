from django.shortcuts import render
from .models import categoryS, Product
# Create your views here.


def index(request , use):
    if use == 1:
        if request.method == 'POST':
            name = request.POST['name']
            cat = request.POST['cat']

            products = Product.objects.all()
            
            if not cat == 'all':
                cate = categoryS.objects.get(name=cat)
                products = Product.objects.filter(cat=cate)
            
            all_products = []
            for product in products:
                product = product
                if name.lower() in product.name.lower():
                    all_products.append(product)
            

            context = {
                'cats': categoryS.objects.all(),
                'Products': all_products,
            }
            return render(request, 'store/index.html', context)
        else:
            context = {
                'cats': categoryS.objects.all(),
                'Products':Product.objects.all()
            }
            return render(request, 'store/index.html', context)
    if use == 2:
            context = {
                'cats': categoryS.objects.all(),
                'Products':Product.objects.filter(price=0)
            }
            return render(request, 'store/index.html', context)
    if use == 3:
            products_all = []
            p = Product.objects.filter(price=0)

            for i in Product.objects.all():
                 if not i in p:
                      products_all.append(i)
            context = {
                'cats': categoryS.objects.all(),
                'Products': products_all,
            }
            return render(request, 'store/index.html', context)



# def Free(request):

        



