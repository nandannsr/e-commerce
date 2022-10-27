from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments/', views.payments,name='payments'),
    path('order_complete/',views.order_complete,name='order_complete'),
    path('cod/<int:order_id>/',views.cod,name='cod'),
    path('cancel_order/<int:order_id>/',views.cancel_order,name='cancel_order'),
    path('return-order',views.return_order,name='return-order'),
    
    #Coupon User application
    path('applycoupon/',views.apply_coupon,name='applycoupon'),
    path('removecoupon/',views.remove_coupon,name='removecoupon'),
]