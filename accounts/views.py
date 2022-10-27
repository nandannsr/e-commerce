from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.views.decorators.cache import cache_control
from category.models import Category
from accounts.models import Account
from category.form import CategoryForm
from brand.models import Brand
from product.models import Product
from brand.form import BrandForm
from product.form import ProductForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from orders.models import BrandOffer, CategoryOffer, Coupon, ProductOffer
from orders.form import BrandOfferForm, CategoryOfferForm, ProductOfferForm, CouponForm
from orders.models import Order, STATUS1, OrderProduct
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
import calendar
import csv
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.user.is_authenticated:
         return redirect(adminhome)
    
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=username, password=password, is_superuser=True)

        if user is not None:
            # request.session['username'] = username
            auth.login(request, user)
            return redirect(adminhome)

        else:
            messages.error(request, 'invalid credential')
            return redirect(index)

    return render(request, 'admin/adminlogin.html')

@login_required(login_url= 'index')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminhome(request,total_orders=0,profit = 0):
    income = 0
    New = 0
    Cancelled = 0
    Returned = 0
    Delivered  = 0
    waiting = 0  
    orders = Order.objects.filter(status='Delivered')
    for order in orders:
        income += order.order_total
    total_orders = Order.objects.all().count() 
    user_count = Account.objects.all().count()
    prod_count = Product.objects.all().count()
    cat_count = Category.objects.all().count()
    brand_count = Brand.objects.all().count()
    queryset = Order.objects.all()
    for i in queryset:
            if i.status == "New":
                New = New + 1
            elif i.status == "Cancelled":
                Cancelled += 1
            elif i.status == "Returned":
                Returned += 1
            elif i.status == "Delivered":
                Delivered += 1
            elif i.status == "Return pending":
                waiting += 1
        
    profit = (income)*0.53
    context = {
        'total_orders': total_orders,
        'income': income,
        'profit': profit,
        'user_count':user_count,
        'new':New,
        'delivered':Delivered,
        'cancelled':Cancelled,
        'returned':Returned,
        'waiting':waiting,
        'prod_count':prod_count,
        'cat_count':cat_count,
        'brand_count':brand_count,
    }
    return render(request,'admin/adminhome.html', context)
    
    
@login_required(login_url= 'index')    
def adminlogout(request):
    # if 'username' in request.session:
    # request.session.flush()
    auth.logout(request)
    return redirect(index)

@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categoryList(request):
    # if 'username' in request.session:
    values = Category.objects.all().order_by('id')
    return render(request, 'admin/admincategory.html', {'values': values})
    # return redirect(admin_login)
    
    
@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addcategory(request):
    # if 'username' in request.session:

    if request.method == "POST":
        cat_form = CategoryForm(request.POST, request.FILES)
        if cat_form.is_valid():
            cat_form.save()
            messages.success(request, 'Your category has been added sucessfully')
        else:
            messages.error(request, 'Error')

        return redirect(categoryList)
    cat_form = CategoryForm()
    cats = Category.objects.all()
    context = {'cat_form': cat_form, 'cats': cats}
    return render(request, 'admin/addcategory.html', context)

    # return redirect(admin_login)
    
@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editcategory(request, id):
    # if 'username' in request.session:
    category = Category.objects.get(id=id)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)

        if form.is_valid():
            form.save()
            return redirect(categoryList)
    else:

        return render(request, 'admin/categoryedit.html', {'form': form})
    # else:
    #     return redirect(admin_login)
    
@login_required(login_url= 'index') 
def deletecategory(request, id):
    # if 'username' in request.session:
    my_cat = Category.objects.get(id=id)
    my_cat.delete()
    return redirect(categoryList)
    # else:
    #     return redirect(admin_login)
    
@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def brandList(request):
    # if 'username' in request.session:
    values = Brand.objects.all().order_by('id')
    return render(request, 'admin/brandlist.html', {'values': values})
    # return redirect(admin_login)
    
@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addbrand(request):
    # if 'username' in request.session:

    if request.method == "POST":
        brand_form = BrandForm(request.POST, request.FILES)
        if brand_form.is_valid():
            brand_form.save()
            messages.success(request, 'Your brand has been added sucessfully')
        else:
            messages.error(request, 'Error')

        return redirect(brandList)
    brand_form = BrandForm()
    brands = Brand.objects.all()
    context = {'brand_form': brand_form, 'brands': brands}
    return render(request, 'admin/addbrand.html', context)

    # return redirect(admin_login)
@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editbrand(request, id):
    # if 'username' in request.session:
        brand = Brand.objects.get(id=id)
        form = BrandForm(instance=brand)
        if request.method == 'POST':
            form = BrandForm(request.POST, request.FILES, instance=brand)

            if form.is_valid():
                form.save()
                return redirect(brandList)
        else:

            return render(request, 'admin/brandedit.html', {'form': form})
    # else:
    #     return redirect(admin_login)
    
def deletebrand(request, id):
    # if 'username' in request.session:
    my_brand = Brand.objects.get(id=id)
    my_brand.delete()
    return redirect(brandList)
    # else:
    #     return redirect(admin_login)    

@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def productList(request):
    # if 'username' in request.session:
    values = Product.objects.all().order_by('id')
    paginator = Paginator(values,3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    return render(request, 'admin/adminproduct.html', {'values': paged_products})
    # return redirect(admin_login)
    
@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editproduct(request, id):
    # if 'username' in request.session:
    product = Product.objects.get(id=id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect(productList)
    else:

        return render(request, 'admin/productedit.html', {'form': form})
    # else:
    #     return redirect(admin_login)
    
@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addproduct(request):
    # if 'username' in request.session:

    if request.method == "POST":
        prod_form = ProductForm(request.POST, request.FILES)
        if prod_form.is_valid():
            prod_form.save()
            messages.success(request, 'Your category has been added sucessfully')
        else:
            messages.error(request, 'Error')

        return redirect(productList)
    prod_form = ProductForm()

    context = {'prod_form': prod_form}
    return render(request, 'admin/addproduct.html', context)


@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteproduct(request, id):
    # if 'username' in request.session:
        my_product = Product.objects.get(id=id)
        my_product.delete()
        return redirect(productList)
    # else:
    #     return redirect(admin_login)

    
@login_required(login_url= 'index')     
def userlist(request):
    
    users = Account.objects.all().order_by('id')
    return render(request, 'admin/userlist.html', {'users': users})


@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blockuser(request, id):
    # if 'username' in request.session:
        user_instance = Account.objects.get(id=id)
        user_instance.is_active=False
        user_instance.is_blocked=True
        user_instance.save()
        messages.info(request,"user is successfully blocked")
        return redirect(userlist)
    
    
@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def unblockuser(request, id):
    # if 'username' in request.session:
        user_instance = Account.objects.get(id=id)
        user_instance.is_active=True
        user_instance.is_blocked=False
        user_instance.save()
        messages.info(request, 'user is successfully unblocked')
        return redirect(userlist)
    
# Start of Offer management functions

@login_required(login_url= 'index')     
def brandofferlist(request):
    
    offerlist = BrandOffer.objects.order_by("id").all()
    return render(request, 'admin/adminbrandoffers.html', {'offers':offerlist})

@login_required(login_url= 'index') 
def addbrandoffer(request):
    if request.method == "POST":
        brand_form = BrandOfferForm(request.POST)
        if brand_form.is_valid():
            brand_form.save()
            messages.success(request, 'Your offer has been added sucessfully')
        else:
            messages.error(request, 'Error')

        return redirect(brandofferlist)
    brand_form = BrandOfferForm()

    context = {'brand_form': brand_form}
    return render(request, 'admin/addbrandoffers.html', context)

@login_required(login_url= 'index') 
def editbrandoffer(request,id):
    offer = BrandOffer.objects.get(id=id)
    form = BrandOfferForm(instance=offer)
    if request.method == 'POST':
        form = BrandOfferForm(request.POST, request.FILES, instance=offer)

        if form.is_valid():
            form.save()
            return redirect(brandofferlist)
    else:

        return render(request, 'admin/editbrandoffers.html', {'form': form})

@login_required(login_url= 'index')  
@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def deletebrandoffer(request, id):
     offer = BrandOffer.objects.get(id=id)
     offer.delete()
     return redirect(brandofferlist)
 
@login_required(login_url= 'index')  
def categoryofferlist(request):
    
    offerlist = CategoryOffer.objects.order_by("id").all()
    return render(request, 'admin/admincategoryoffers.html', {'offers':offerlist})

@login_required(login_url= 'index') 
def addcategoryoffer(request):
    if request.method == "POST":
        cat_form = CategoryOfferForm(request.POST)
        if cat_form.is_valid():
            cat_form.save()
            messages.success(request, 'Your offer has been added sucessfully')
        else:
            messages.error(request, 'Error')

        return redirect(categoryofferlist)
    cat_form = CategoryOfferForm()

    context = {'cat_form': cat_form}
    return render(request, 'admin/addcategoryoffer.html', context)

@login_required(login_url= 'index') 
def editcategoryoffer(request,id):
    offer = CategoryOffer.objects.get(id=id)
    form = CategoryOfferForm(instance=offer)
    if request.method == 'POST':
        form = CategoryOfferForm(request.POST,instance=offer)

        if form.is_valid():
            form.save()
            return redirect(categoryofferlist)
    else:

        return render(request, 'admin/editcategoryoffer.html', {'form': form})
    
    
@login_required(login_url= 'index')  
@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def deletecategoryoffer(request, id):
     offer = CategoryOffer.objects.get(id=id)
     offer.delete()
     return redirect(categoryofferlist)
 
@login_required(login_url= 'index')  
def productofferlist(request):
    
    offerlist = ProductOffer.objects.order_by("id").all()
    return render(request, 'admin/adminproductoffers.html', {'offers':offerlist})

@login_required(login_url= 'index') 
def addproductoffer(request):
    if request.method == "POST":
        pod_form = ProductOfferForm(request.POST)
        if pod_form.is_valid():
            pod_form.save()
            messages.success(request, 'Your offer has been added sucessfully')
        else:
            messages.error(request, 'Error')

        return redirect(categoryofferlist)
    pod_form = ProductOfferForm()

    context = {'pod_form': pod_form}
    return render(request, 'admin/addproductoffer.html', context)

@login_required(login_url= 'index') 
def editproductoffer(request,id):
    offer = ProductOffer.objects.get(id=id)
    form = ProductOfferForm(instance=offer)
    if request.method == 'POST':
        form = ProductOfferForm(request.POST,instance=offer)

        if form.is_valid():
            form.save()
            return redirect(productofferlist)
    else:

        return render(request, 'admin/editproductoffer.html', {'form': form})
    
@login_required(login_url= 'index')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
def deleteproductoffer(request, id):
     offer = ProductOffer.objects.get(id=id)
     offer.delete()
     return redirect(productofferlist)
 
#****End of Offer management****#


#Start of Coupon management functions 
@login_required(login_url= 'index') 
def couponlist(request):
    coupons = Coupon.objects.order_by("id").all()
    return render(request, 'admin/admincoupons.html', {'coupons':coupons})

@login_required(login_url= 'index') 
def editcoupons(request, id):
    coupon = Coupon.objects.get(id=id)
    form = CouponForm(instance=coupon)
    if request.method == 'POST':
        form = CouponForm(request.POST,instance=coupon)

        if form.is_valid():
            form.save()
            return redirect(couponlist)
    else:

        return render(request, 'admin/editcoupons.html', {'form': form})
    
@login_required(login_url= 'index')     
def addcoupons(request):
    if request.method == "POST":
        coup_form = CouponForm(request.POST)
        if coup_form.is_valid():
            coup_form.save()
            messages.success(request, 'Your coupon has been added sucessfully')
        else:
            messages.error(request, 'Error')

        return redirect(couponlist)
    coup_form = CouponForm()

    context = {'coup_form': coup_form}
    return render(request, 'admin/addcoupons.html', context)

@login_required(login_url= 'index')
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def deletecoupon(request,id):
     coupon = Coupon.objects.get(id=id)
     coupon.delete()
     return redirect(couponlist)
 
#****End of Coupon management****#

#Admin Order management#
@login_required(login_url= 'index') 
def order_list(request):
    orders = Order.objects.order_by('-created_at').all()
    context = {
        'orders':orders,
        "status": STATUS1,
    } 
    return render(request,'admin/admin_orders.html',context)

@login_required(login_url= 'index') 
def delivered_status(request):
    if request.method == 'POST':
        order_id = int(request.POST.get('orderID'))
        orders = Order.objects.get(id=order_id)
        orders.status = 'Delivered'
        orders.payment.status = 'Successful'
        orders.payment.save()
        orders.save()
        return JsonResponse({'status':"updated"})
    
@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cancel_status(request):
    if request.method == 'POST':
        orderID = int(request.POST.get('orderID'))
        order  = Order.objects.get(id=orderID)
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    
    
    for item in ordered_products:
        
         product = Product.objects.get(id=item.product_id)
         product.stock += item.quantity
         product.save()
         item.ordered = 'False'
         item.save()
         
    order.status = 'Cancelled'
    order.payment.status = 'Refunded'
    order.payment.save()
    
    order.is_ordered = 'False'
    order.save()
    return JsonResponse({'status':"updated"})

@login_required(login_url= 'index') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def return_status(request):
    if request.method == 'POST':
        orderID = int(request.POST.get('orderID'))
        order  = Order.objects.get(id=orderID)
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    
    
    for item in ordered_products:
        
         product = Product.objects.get(id=item.product_id)
         product.stock += item.quantity
         product.save()
         item.ordered = 'False'
         item.save()
         
    order.status = 'Returned'
    order.payment.status = 'Refunded'
    order.payment.save()
    
    order.is_ordered = 'False'
    order.save()
    return JsonResponse({'status':"updated"})


@login_required(login_url= 'index') 
def order_search(request):
     if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            orders= Order.objects.order_by('-created_at').filter(status__icontains=keyword)
            
            context ={
            'orders':orders
            }
            return render(request, 'admin/ordersearch.html', context)
        else:
            return redirect(order_list)
        
#*********************************#

#Admin Sales report and download views#
        
@login_required(login_url= 'index')        
def sales_report(request):
    if request.user.is_authenticated and request.user.is_admin:
        product = Product.objects.all()
        context = {"product": product}
        return render(request, "admin/salesreport.html", context)
    else:
        return redirect(index)
    
@login_required(login_url= 'index')     
def sales_export_csv(request):
    if request.user.is_authenticated and request.user.is_admin:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=products.csv"

        writer = csv.writer(response)
        products = Product.objects.all().order_by("-id")

        writer.writerow(
            [
                "Product",
                "Brand",
                "Category",
                "Stock",
                "Price",
                "Sales Count",
                "Revenue",
                "Profit",
            ]
        )

        for product in products:
            writer.writerow(
                [
                    product.product_name,
                    product.brand.brand_name,
                    product.category.category_name,
                    product.stock,
                    product.price,
                    product.get_count(),
                    product.get_revenue(),
                    product.get_profit(),
                ]
            )
        return response
    else:
        return redirect("/")