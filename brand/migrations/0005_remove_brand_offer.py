# Generated by Django 4.1.1 on 2022-10-16 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0004_brand_offer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='offer',
        ),
    ]