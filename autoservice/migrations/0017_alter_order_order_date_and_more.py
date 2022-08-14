# Generated by Django 4.0.4 on 2022-05-12 08:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0016_alter_order_order_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 11, 10, 36, 764997, tzinfo=utc), verbose_name='Order Date'),
        ),
        migrations.AlterField(
            model_name='ordersreview',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 11, 10, 36, 769985, tzinfo=utc), verbose_name='Order Date'),
        ),
    ]