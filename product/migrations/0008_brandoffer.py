# Generated by Django 4.1.1 on 2022-10-16 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0005_remove_brand_offer'),
        ('product', '0007_remove_product_brand_offer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('brand_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brand.brand')),
            ],
        ),
    ]