from distutils.command.build_scripts import first_line_re
from itertools import product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.views.decorators.cache import cache_control
from requests import post
from category.models import Category
from accounts.models import Account, UserProfile
from .models import *
from .mixins import *
from orders.models import Order, OrderProduct
from product.models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .form import RegisterForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from cart.views import _cart_id
import requests
from django.db.models import Q
from brand.models import Brand


# Create your views here.

def register(request):
    
    if request.method == 'POST':
        forms = RegisterForm(request.POST)
        if forms.is_valid():
            first_name = forms.cleaned_data['first_name']
            last_name = forms.cleaned_data['last_name']
            phone_number = forms.cleaned_data['phone_number']
            email = forms.cleaned_data['email']
            password = forms.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email, username=username, password=password)
            user.save()
            request.session['phone_number'] = phone_number
            send(phone_number)
            return redirect(otpverify)

            
    else:
        forms = RegisterForm()
    context ={
        'forms' : forms,
        
        }
           
    return render(request,'user/userregister.html', context)       
    
  
def userlogin(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            if user.is_admin:
                messages.error(request,'Invalid Login Credentials')
                return redirect(userlogin) 
            try:
              cart = Cart.objects.get(cart_id=_cart_id(request))  
              is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
              if is_cart_item_exists:
                  cart_item = CartItem.objects.filter(cart=cart)
                  
                  #getting the product variations by cart id
                  product_variation = []
                  for item in cart_item:
                       variation = item.variations.all()
                       product_variation.append(list(variation))
                       
                  #get the cart items from the user to access his variations
                  
                  cart_item = CartItem.objects.filter(user=user)
                  ex_var_list = []
                  id  = []
                  for item in cart_item:
                      existing_variation =item.variations.all()
                      ex_var_list.append(list(existing_variation))
                      id.append(item.id)
                      
                  for pr in product_variation:
                      if pr in ex_var_list:
                          index = ex_var_list.index(pr)
                          item_id = id[index]
                          item = CartItem.objects.get(id=item_id)
                          item.quantity += 1
                          item.user = user
                          item.save()
                          
                      else:
                          cart_item  = CartItem.objects.filter(cart=cart)
                          for item in cart_item:
                            item.user = user
                            item.save()
                
            except:
                pass
            
            auth.login(request, user)
            # messages.success(request,'You are now logged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                
            except:
                return redirect(userhome)
                
            
        else:
            messages.error(request,'Invalid Login Credentials')
            return redirect(userlogin)
    return render(request,'user/userlogin.html')  
    




 
def userhome(request):
    products = Product.objects.filter(category__category_name="Chairs", is_available=True)[:]
    context= {
        'products': products
    }
    return render(request,'user/home.html', context)  


@login_required(login_url= 'userlogin')
def userlogout(request):
    auth.logout(request)
    messages.success(request,'You are logged out')
    return redirect(userhome)

#OTP views#
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def otpverify(request):
    if request.method == 'POST':
       phone_otp = request.POST['otp']
       user = Account.objects.get(phone_number=request.session['phone_number'])
       if check(request.session['phone_number'],phone_otp):
           user.is_active=True
           user.is_phone_verified=True
           user.save()
           
           #creating the user profile
           profile = UserProfile()
           profile.user_id = user.id
           profile.profile_picture = 'default/defaultprofile.png'
           profile.save()
           messages.success(request, 'Registration successful')
           return redirect(register)
       
       else:
           print('failed')
           messages.info(request,'otp verification failed')
           user.delete()
           return redirect(register)
           
    else:
        return render(request,'user/otp_verify.html')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)        
def otp_try_again(request):
      user = Account.objects.get(phone_number=request.session['phone_number'])
      user.delete()
      messages.info(request,'Please try again')
      return redirect(register)
  
#****************#  
     
@login_required(login_url= 'userlogin')   
def userprofile(request):
    orders = Order.objects.order_by('created_at').filter(user_id=request.user.id)
    orders_count = orders.count()
    
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
        }
    return render(request, 'user/userdashboard.html',context)


def shop(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        
        products = Product.objects.filter(category=categories, is_available=True)
        # for checking if offer exists or not for the product
        for product in products:  
            if product.Offer_Price():
                new = Product.Offer_Price(product)
                product.offer_price = new["new_price"]
                product.percentage = new["discount"]
                product.save()
            else:
                product.offer_price = 0
                product.save()
        paginator = Paginator(products,8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        
        products = Product.objects.all().filter(is_available=True).order_by("id")
        # for checking if offer exists or not for the product
        for product in products:  
            if product.Offer_Price():
                new = Product.Offer_Price(product)
                product.offer_price = new["new_price"]
                product.percentage = new["discount"]
                product.save()
            else:
                product.offer_price = 0
                product.save()
        paginator = Paginator(products,8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    return render(request, 'user/usershop.html', {'values': paged_products})

def brand_shop(request, brand_slug=None):
    brands = None
    products = None
    
    if brand_slug != None:
        brands = get_object_or_404(Brand, slug=brand_slug)
        
        products = Product.objects.filter(brand=brands, is_available=True)
        # for checking if offer exists or not for the product
        print(products)
        if products:
            
            for product in products:  
              if product.Offer_Price():
                  
                new = Product.Offer_Price(product)
                product.offer_price = new["new_price"]
                product.percentage = new["discount"]
                product.save()
                
              else:
                product.offer_price = 0
                product.save()
                
            paginator = Paginator(products,8)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
        else:
            messages.info(request,"No items found") 
            return redirect(shop)   
    else:
        return redirect(shop)
        
    return render(request, 'user/usershop.html', {'values': paged_products})

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            context ={
            'values':products
            }
            return render(request, 'user/usersearch.html', context)
        else:
            return redirect(shop)
        
    else:
        return redirect(shop)

def productview(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e    
    
    context = {
        'single_product': single_product
    }
    return render(request,'user/productview.html',context)

@login_required(login_url= 'userlogin')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders':orders
    } 
    return render(request, 'user/orderlist.html', context)

@login_required(login_url= 'userlogin')
def editprofile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('editprofile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile': userprofile,
    }    
    return render(request, 'user/editprofile.html', context)

@login_required(login_url= 'userlogin')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)
        
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter correct password')
                return redirect('change_password')
        else:
            messages.error(request, 'Passwords not matching')
            return redirect('change_password')
    return render(request, 'user/changepassword.html')

@login_required(login_url= 'userlogin')
def order_detail(request,order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request,'user/profileorderdetail.html', context)
    