# Generated by Django 2.2.7 on 2020-03-17 17:15

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0005_auto_20200316_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='geometry',
            field=django.contrib.gis.db.models.fields.PointField(extent=(31.0, 49.0, 33.0, 49.0), help_text='<em>Просто поставте маркер на карту</em>', srid=4326, verbose_name='Місце на мапі'),
        ),
    ]
