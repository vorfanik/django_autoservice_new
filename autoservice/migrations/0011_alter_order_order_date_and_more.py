# Generated by Django 4.0.4 on 2022-05-11 09:35

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0010_alter_order_order_date_ordersreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 11, 12, 35, 19, 797632, tzinfo=utc), verbose_name='Order Date'),
        ),
        migrations.AlterField(
            model_name='ordersreview',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 11, 12, 35, 19, 799614, tzinfo=utc), verbose_name='Order Date'),
        ),
        migrations.AlterField(
            model_name='ordersreview',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='autoservice.order'),
        ),
    ]
