# Generated by Django 3.2 on 2021-06-10 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availableproducts',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='products.products'),
        ),
    ]
