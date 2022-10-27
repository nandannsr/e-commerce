
from django.db import models



# Create your models here.
from brand.models import Brand
from category.models import Category
import uuid
from django.urls import reverse
from django.db.models import Sum
from django.utils import timezone
from django.apps import apps



class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(max_length=500, blank=True)
    details = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    offer_price = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    images = models.ImageField(upload_to='pics/products')
    images1 = models.ImageField(upload_to='pics/products')
    images2 = models.ImageField(upload_to='pics/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    
    def get_url(self):
        return reverse('productview',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name
    
    def Offer_Price(self):
        try:
            if self.productoffer.is_valid:
                offer_price = (self.price * self.productoffer.discount) / 100
                new_price = self.price - offer_price
                return {
                    "new_price": new_price,
                    "discount": self.productoffer.discount,
                }
            raise
        except:
            try:
                if self.brand.brandoffer.is_valid:
                    offer_price = (self.price * self.brand.brandoffer.discount) / 100
                    new_price = self.price - offer_price
                    print(offer_price)
                    return {
                        "new_price": new_price,
                        "discount": self.brand.brandoffer.discount,
                    }
                raise
            except:
                try:
                    if self.category.categoryoffer.is_valid:
                        offer_price = (
                            self.price * self.category.categoryoffer.discount
                        ) / 100
                        new_price = self.price - offer_price
                        return {
                            "new_price": new_price,
                            "discount": self.category.categoryoffer.discount,
                        }
                    raise
                except:
                    pass
        
    def get_count(self, month=timezone.now().month):
        orderproduct = apps.get_model("orders", "OrderProduct")
        count_item = orderproduct.objects.filter(product=self, created_at__month=month, order__status='Delivered').count()
        return count_item

    def get_revenue(self, month=timezone.now().month):
        orderproduct = apps.get_model("orders", "OrderProduct")
        count_item = orderproduct.objects.filter(product=self, created_at__month=month, order__status='Delivered').count()
        revenue = float(count_item) * self.offer_price
        return revenue

    def get_profit(self, month=timezone.now().month):
        orderproduct = apps.get_model("orders", "OrderProduct")
        count_item = orderproduct.objects.filter(product=self, created_at__month=month, order__status='Delivered').count()
        if self.Offer_Price:
          revenue = float(count_item) * self.offer_price
        else:
           revenue = float(count_item) * self.price   
        profit = revenue * 0.43
        return profit
        
                
variation_category_choice = (
     ('color', 'color'),
     ('size', 'size')
)

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size',is_active=True)

    
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)    
    
    objects = VariationManager()    
    
    def __str__(self):
        return self.variation_value

        
    