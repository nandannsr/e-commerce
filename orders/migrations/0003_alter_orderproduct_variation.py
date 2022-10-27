# Generated by Django 4.1.1 on 2022-10-06 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_variation'),
        ('orders', '0002_remove_orderproduct_color_remove_orderproduct_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='variation',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='product.variation'),
        ),
    ]