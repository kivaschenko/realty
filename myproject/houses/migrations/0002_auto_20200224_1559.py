# Generated by Django 2.2.7 on 2020-02-24 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='currency',
            field=models.CharField(choices=[('UAH', 'грн.')], default='UAH', max_length=3, verbose_name='Валюта'),
        ),
    ]
