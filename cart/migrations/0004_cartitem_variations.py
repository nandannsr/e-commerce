# Generated by Django 4.1.1 on 2022-10-04 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_variation'),
        ('cart', '0003_remove_cartitem_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='product.variation'),
        ),
    ]