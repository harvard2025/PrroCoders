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

        



from django.shortcuts import render, redirect
from .models import Product, categoryS
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_staff)  # Only staff can add products
def add_product(request):
    if request.method == 'POST':
        # Process form data
        image = request.FILES.get('image')
        name = request.POST.get('name')
        description = request.POST.get('description')
        link = request.POST.get('link')
        file = request.FILES.get('file')
        is_active = request.POST.get('isActive') == 'on'
        by = request.POST.get('by')
        price = int(request.POST.get('price'))
        cat_id = request.POST.get('cat')
        
        category = categoryS.objects.get(id=cat_id)
        
        Product.objects.create(
            image=image,
            name=name,
            description=description,
            Link=link,
            File=file,
            isActive=is_active,
            By=by,
            price=price,
            cat=category
        )
        
        return redirect('store:store', use=1)  # Redirect to store page
    
    # GET request - show form
    categories = categoryS.objects.all()
    return render(request, 'store/add_product.html', {'categories': categories})





from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # اختياري: السماح فقط لصاحب المنتج أو الأدمن بالحذف
    if request.user.is_superuser or request.user.username == product.By:
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('store:store', use=1)  # رجع للقائمة أو أي مكان مناسب
    else:
        messages.error(request, 'You are not authorized to delete this product.')
        return redirect('store:product_detail', product_id=product_id)
