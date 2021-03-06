# Generated by Django 3.2 on 2021-06-09 02:38

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipments',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('SHIPPED', 'SHIPPED'), ('DELIVERED', 'DELIVERED')], max_length=30)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='orders.orders')),
            ],
            options={
                'db_table': 'shipments',
            },
        ),
    ]
