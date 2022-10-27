from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from cart.models import CartItem, Cart
from cart.views import cart
from product.models import Product
from user.views import shop
from .form import OrderForm
from . models import Coupon, Order, OrderProduct, Payment, UsedCoupon
import datetime
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import razorpay
from user.views import my_orders
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
# Create your views here.

@login_required(login_url="userlogin")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False,order_number=body['orderID'])
    #Store transactiondetails inside Payment Model
    payment = Payment(
        user= request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
           
    )
    payment.save()
    
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    #move the cart items to Order Product Table
    cart_items = CartItem.objects.filter(user=request.user)
    
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        if item.product.Offer_Price(): #checking offers
                offer_price = Product.Offer_Price(item.product)
                price = offer_price["new_price"]
                orderproduct.product_price = price
        else:
                orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
    
    #Reduce the quantity of the sold products
    
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
        
    
    #clear the cart
    CartItem.objects.filter(user=request.user).delete()
    
    
    #send order number and transaction to sendData method via Jsonresponse
    
    data = {
        "order_number": order.order_number,
        "transID": payment.payment_id,  
    }
    return JsonResponse(data) 
    
    # return render(request, 'cart/payments.html')
    
@login_required(login_url='userlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def place_order(request, total=0, quantity=0, reduction=0):
    
    current_user = request.user
    
    # if the cart is less than or equal to 0, then redirect to shop view
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect(shop)
    
    grand_total = 0
    tax = 0
    if "coupon_code" in request.session:
        coupon = Coupon.objects.get(coupon_code=request.session["coupon_code"])
        reduction = coupon.discount

    else:
        coupon = None
        reduction = 0
    for cart_item in cart_items:
        if cart_item.product.Offer_Price():
                offer_price = Product.Offer_Price(cart_item.product)
                print(offer_price["new_price"])
                total = total + (offer_price["new_price"] * cart_item.quantity)
                print(total)
        else:
                total = total + (cart_item.product.price * cart_item.quantity)

        quantity += cart_item.quantity
        
    tax = (2 * total)/100
    grand_total = total + tax - reduction  
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            
            #store all the billing information inside order Table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']  
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            #   Generate the order nnumber
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id) 
            data.order_number = order_number
            data.save()
            
            order  = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
                'coupon':coupon,
            }
            return render(request,'cart/payments.html', context)
        
        else:
       
            return redirect('checkout')           
        
       
@login_required(login_url="userlogin")  
@cache_control(no_cache=True, must_revalidate=True, no_store=True)      
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    
    
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        
        subtotal = 0
        for i in ordered_products:
          subtotal += i.product_price * i.quantity 
          
        payment = Payment.objects.get(payment_id=transID)
        context = {
            'order':order,
            'ordered_products':ordered_products,
            'order_number': order_number,
            'transID': payment.payment_id,
            'payment':payment,
            'subtotal': subtotal,
         }
        if "coupon_code" in request.session:
                print("coupon found ")
                used_coupons = UsedCoupon()
                coupon = Coupon.objects.get(coupon_code=request.session["coupon_code"])
                print(coupon)
                used_coupons.coupon = coupon
                used_coupons.user = request.user
                used_coupons.save()
                print(request.session["coupon_code"])
                del request.session["coupon_code"]
                
        return render(request, 'cart/order_complete.html',context)

    except( Payment.DoesNotExist, Order.DoesNotExist):
         return redirect('userhome')
     
     
    # For Cash on delivery
@login_required(login_url="userlogin")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cod(request,order_id):
    
     order = Order.objects.get(user=request.user, is_ordered=False,order_number=order_id)
    #Store transactiondetails inside Payment Model
     payment = Payment(
        user= request.user,
        payment_method = 'Cash On delivery',
        amount_paid = order.order_total,
        status = 'Payment Pending',
           
    )
     payment.save()
    
     order.payment = payment
     order.is_ordered = True
     order.save()
    
    #move the cart items to Order Product Table
     cart_items = CartItem.objects.filter(user=request.user)
    
     for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        if item.product.Offer_Price(): # checking offers
                offer_price = Product.Offer_Price(item.product)
                price = offer_price["new_price"]
                orderproduct.product_price = price
        else:
                orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
    
    #Reduce the quantity of the sold products
    
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
        
    
    #clear the cart
     CartItem.objects.filter(user=request.user).delete()
    
     ordered_products = OrderProduct.objects.filter(order_id=order.id)
     subtotal = 0
     for i in ordered_products:
         subtotal += i.product_price * i.quantity 
    
    
     data = {
        'order':order,
        'payment':payment,
        'ordered_products': ordered_products,
        'subtotal': subtotal,
        'order_number': order_id
    }
     if "coupon_code" in request.session:
                print("coupon found ")
                used_coupons = UsedCoupon()
                coupon = Coupon.objects.get(coupon_code=request.session["coupon_code"])
                print(coupon)
                used_coupons.coupon = coupon
                used_coupons.user = request.user
                used_coupons.save()
                print(request.session["coupon_code"])
                del request.session["coupon_code"]
                
     return render(request, 'cart/cod_detail.html', data)
 
 # To cancel the user order
@login_required(login_url="userlogin") 
def cancel_order(request,order_id):
    order  = Order.objects.get(user=request.user, is_ordered=True, order_number=order_id)
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    
    
    for item in ordered_products:
        
         product = Product.objects.get(id=item.product_id)
         product.stock += item.quantity
         product.save()
         item.ordered = 'False'
         item.save()
         
    order.status = 'Cancelled'
    order.payment.status = 'Cancelled'
    order.payment.save()
    
    order.is_ordered = 'False'
    order.save()
    return redirect(my_orders)

#return the order from user side
@login_required(login_url="userlogin")
def return_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('orderNO')
        orders = Order.objects.get(order_number=order_id)
        orders.status = 'Return pending'
        orders.payment.status = 'Refund Pending'
        orders.payment.save()
        orders.save()
        return JsonResponse({'status':"updated"})

# Coupon Management #   
@login_required(login_url="userlogin") 
def apply_coupon(request):
     
    if request.method == "POST":

        coupon_code = request.POST.get("code")

        try:
            if "code" in request.POST:
                if Coupon.objects.get(coupon_code=coupon_code, is_active=True):
                    coupon_exist = Coupon.objects.get(coupon_code=coupon_code)
                    try:
                        used_coupon = UsedCoupon.objects.get(
                            user=request.user, coupon=coupon_exist
                        )
                        if used_coupon is not None:
                            messages.error(request, "Coupon already used!!")
                            return JsonResponse({'status':"updated"})

                    except:

                        print("pass")
                        request.session["coupon_code"] = coupon_code
                        return JsonResponse({'status':"updated"})
            else:
                pass
                return JsonResponse({'status':"updated"})
        except:
            messages.error(request, "Invalid Coupon!!")
            return JsonResponse({'status':"updated"})

    return redirect(cart)

@login_required(login_url="userlogin")
def remove_coupon(request):
  if request.method == "POST":
         
    del request.session["coupon_code"]
    return JsonResponse({'status':"updated"})