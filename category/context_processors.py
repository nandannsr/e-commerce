from .models import Category
from brand.models import Brand

def menu_links(request):
     links = Category.objects.all()
     return dict(links=links) 

def brand_links(request):
     blinks = Brand.objects.all()
     return dict(blinks=blinks)