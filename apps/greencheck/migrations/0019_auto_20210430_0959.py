# Generated by Django 3.2 on 2021-04-30 09:59

import datetime
import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greencheck', '0018_auto_20210430_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailystat',
            name='extra_data',
            field=models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder),
        ),
        migrations.AlterField(
            model_name='dailystat',
            name='stat_date',
            field=models.DateField(default=datetime.datetime(2021, 4, 29, 9, 59, 14, 513439), verbose_name='Date for stats'),
        ),
    ]