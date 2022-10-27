from django import forms
from .models import Brand


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('brand_name', 'slug', 'brand_logo')
        
    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
       
            
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'