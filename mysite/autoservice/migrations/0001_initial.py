# Generated by Django 4.0.4 on 2022-05-03 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AutoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=200, verbose_name='Brand')),
                ('car_model', models.CharField(max_length=200, verbose_name='Model')),
                ('year', models.IntegerField(verbose_name='Year')),
                ('engine', models.CharField(max_length=200, verbose_name='Engine')),
            ],
            options={
                'verbose_name': 'Car model',
                'verbose_name_plural': 'Car models',
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=100, verbose_name='Owner')),
                ('license_plate', models.CharField(max_length=10, verbose_name='License plate')),
                ('vin', models.CharField(help_text='17 Characters <a href="https://www.vindecoderz.com/">VIN code</a>', max_length=20, verbose_name='VIN code')),
                ('auto_model_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.automodel', verbose_name='Car Model')),
            ],
            options={
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='Order Date')),
                ('status', models.CharField(blank=True, choices=[('p', 'Confirmed'), ('v', 'In progress'), ('a', 'Completed'), ('t', 'Canceled')], default='p', help_text='Status', max_length=1)),
                ('car_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.car', verbose_name='Car')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('price', models.FloatField(verbose_name='Price')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='OrderingLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('order_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.order', verbose_name='Order')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.service', verbose_name='Service')),
            ],
            options={
                'verbose_name': 'Order line',
                'verbose_name_plural': 'Order lines',
            },
        ),
    ]
