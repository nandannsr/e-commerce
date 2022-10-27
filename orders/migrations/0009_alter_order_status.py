# Generated by Django 4.1.1 on 2022-10-25 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('Returned', 'Returned'), ('Delivered', 'Delivered'), ('Return pending', 'Return pending'), ('Cancelled', 'Cancelled')], default='New', max_length=50),
        ),
    ]
