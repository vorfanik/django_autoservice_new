# Generated by Django 4.0.4 on 2022-05-19 08:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0022_alter_order_order_date_alter_order_return_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 19, 11, 42, 3, 828626, tzinfo=utc), verbose_name='Order Date'),
        ),
        migrations.AlterField(
            model_name='ordersreview',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 19, 11, 42, 3, 830622, tzinfo=utc), verbose_name='Order Date'),
        ),
    ]
