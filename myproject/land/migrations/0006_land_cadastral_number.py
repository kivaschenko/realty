# Generated by Django 2.2.7 on 2020-03-14 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0005_auto_20200307_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='land',
            name='cadastral_number',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Кадастровий номер'),
        ),
    ]
