# Generated by Django 3.2 on 2021-05-11 12:50

import datetime
from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('greencheck', '0024_auto_20210503_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailystat',
            name='stat_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 10, 12, 50, 39, 273375), verbose_name='Date for stats'),
        ),
        migrations.AlterField(
            model_name='greencheck',
            name='type',
            field=django_mysql.models.EnumField(choices=[('as', 'as'), ('ip', 'ip'), ('none', 'none'), ('url', 'url'), ('whois', 'whois')], default='none'),
        ),
    ]