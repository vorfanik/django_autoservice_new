# Generated by Django 4.0.4 on 2022-05-12 07:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autoservice', '0012_alter_order_order_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 10, 33, 27, 123111, tzinfo=utc), verbose_name='Order Date'),
        ),
        migrations.AlterField(
            model_name='ordersreview',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 10, 33, 27, 127100, tzinfo=utc), verbose_name='Order Date'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(default='default.jpg', upload_to='profile_photo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
