# Generated by Django 4.1.1 on 2022-10-16 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0002_delete_productoffer'),
        ('product', '0004_product_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand_offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='offers.brandoffer'),
        ),
    ]
