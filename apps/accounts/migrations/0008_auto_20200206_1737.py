# Generated by Django 2.2.10 on 2020-02-06 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200206_1105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hostingprovider',
            options={'verbose_name': 'Hosting Provider'},
        ),
        migrations.RemoveField(
            model_name='hostingproviderstats',
            name='id',
        ),
        migrations.AlterField(
            model_name='hostingproviderstats',
            name='hostingprovider',
            field=models.ForeignKey(db_column='id_hp', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.Hostingprovider'),
        ),
    ]