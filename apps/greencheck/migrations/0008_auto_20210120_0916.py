# Generated by Django 2.2.17 on 2021-01-20 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greencheck', '0007_auto_20210120_0805'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='greencheckipapprove',
            name='greencheck__created_23c8a1_idx',
        ),
        migrations.AlterField(
            model_name='greencheck',
            name='greencheck_ip',
            field=models.IntegerField(db_column='id_greencheck'),
        )
    ]