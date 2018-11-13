# Generated by Django 2.1.2 on 2018-11-12 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TaApp', '0004_auto_20181111_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='office_hours',
            field=models.ManyToManyField(null=True, to='TaApp.OfficeHour'),
        ),
        migrations.AlterField(
            model_name='lab',
            name='ta',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='TaApp.Account'),
        ),
    ]
