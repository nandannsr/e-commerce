from django.contrib import admin
from .models import BrandOffer, CategoryOffer, Coupon, Payment, Order, OrderProduct, ProductOffer, UsedCoupon
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered']
    list_filter = ['status','is_ordered']
    search_fields = ['order_number' , 'first_name', 'email']
    
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','payment_id','payment_method','status']
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(BrandOffer)
admin.site.register(ProductOffer)
admin.site.register(CategoryOffer)
admin.site.register(Coupon)
admin.site.register(UsedCoupon)