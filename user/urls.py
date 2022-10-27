from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register, name='register'),
    path('userlogin',views.userlogin, name='userlogin'),
    path('userlogout',views.userlogout, name='userlogout'),
    path('otpverify',views.otpverify,name='otpverify'),
    path('',views.userhome,name='home'),
    path('otp-try-again',views.otp_try_again,name='otp-try-again'),
    
    #User profile management
    path('profile',views.userprofile, name='profile'),
    path('editprofile/',views.editprofile, name='editprofile'),
    path('myorders',views.my_orders, name='myorders'), 
   
    path('change_password',views.change_password,name='change_password'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    
    #Shop views
    path('shop/',views.shop,name='shop'),
    path('category/<slug:category_slug>/',views.shop,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.productview,name='productview'),
    path('search/',views.search, name='search'),
    
    
    
   
    
]