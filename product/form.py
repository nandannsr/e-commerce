from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'product_name', 'slug', 'description','details', 'price', 'images', 'images1', 'images2', 'is_available', 'stock', 'category','brand')
        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['images'].widget.attrs['id'] = 'id_images'
        self.fields['images1'].widget.attrs['id'] = 'id_images1'
        self.fields['images2'].widget.attrs['id'] = 'id_images2'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control-sm'