# Generated by Django 4.0.4 on 2022-05-05 08:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0004_alter_order_order_date_alter_orderingline_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 5, 11, 9, 22, 331587, tzinfo=utc), verbose_name='Order Date'),
        ),
    ]
