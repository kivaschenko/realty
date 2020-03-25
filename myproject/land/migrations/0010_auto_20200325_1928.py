# Generated by Django 2.2.7 on 2020-03-25 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0009_auto_20200317_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='land',
            name='MSZoning',
            field=models.CharField(choices=[('A', 'Присадибна ділянка для будівництва приватного будинку'), ('C', 'Особисте селянське господарство'), ('FV', 'Садова або дачне будівництво'), ('I', 'Комерційна діяльність'), ('RH', 'Під багатоквартирний будинок'), ('RL', 'НИЗЬКА ЩІЛЬНІСТЬ ЗАБУДОВИ'), ('RP', 'Для ведення товарного сільського господарства'), ('RM', 'Приватний будинок + особисте селянське господарство')], default='A', max_length=3, verbose_name='Тип земельної ділянки'),
        ),
        migrations.AlterField(
            model_name='land',
            name='currency',
            field=models.CharField(choices=[('UAH', 'грн.'), ('USD', 'USD')], default='USD', max_length=3, verbose_name='Валюта'),
        ),
    ]
