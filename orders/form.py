from django import forms
from django import forms
from .models import Coupon, Order, BrandOffer, CategoryOffer, ProductOffer

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name', 'email', 'phone', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
            
class BrandOfferForm(forms.ModelForm):
    class Meta:
        model = BrandOffer
        fields = ["brand_name", "discount"]


class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffer
        fields = ["category_name", "discount"]


class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ["product_name", "discount"]
        
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ["coupon_code", "discount", "is_active"]