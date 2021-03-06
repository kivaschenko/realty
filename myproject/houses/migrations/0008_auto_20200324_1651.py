# Generated by Django 2.2.7 on 2020-03-24 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0007_auto_20200317_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='ExterCond',
        ),
        migrations.RemoveField(
            model_name='house',
            name='Exterior',
        ),
        migrations.RemoveField(
            model_name='house',
            name='Fireplace',
        ),
        migrations.RemoveField(
            model_name='house',
            name='FirstFloor',
        ),
        migrations.RemoveField(
            model_name='house',
            name='Foundation',
        ),
        migrations.RemoveField(
            model_name='house',
            name='GarageArea',
        ),
        migrations.RemoveField(
            model_name='house',
            name='GarageCars',
        ),
        migrations.RemoveField(
            model_name='house',
            name='GarageCond',
        ),
        migrations.RemoveField(
            model_name='house',
            name='GarageFinish',
        ),
        migrations.RemoveField(
            model_name='house',
            name='GarageYrBlt',
        ),
        migrations.RemoveField(
            model_name='house',
            name='LotFrontage',
        ),
        migrations.RemoveField(
            model_name='house',
            name='LowQualFinSF',
        ),
        migrations.RemoveField(
            model_name='house',
            name='PoolArea',
        ),
        migrations.RemoveField(
            model_name='house',
            name='PoolQC',
        ),
        migrations.RemoveField(
            model_name='house',
            name='SecondFloor',
        ),
        migrations.RemoveField(
            model_name='house',
            name='YearBuilt',
        ),
        migrations.RemoveField(
            model_name='house',
            name='YearRenovation',
        ),
        migrations.RemoveField(
            model_name='house',
            name='satellite_tv',
        ),
        migrations.AddField(
            model_name='house',
            name='CadastrNumber',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Кадастровий номер'),
        ),
        migrations.AlterField(
            model_name='house',
            name='Bedroom',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Кількість спалень'),
        ),
        migrations.AlterField(
            model_name='house',
            name='Fence',
            field=models.CharField(choices=[('GdPrv', 'Добре захищена приватність'), ('MnPrv', 'Мінімальна приватність'), ('BadPrv', 'Погано захищена приватність'), ('NA', 'Немає огорожі')], default='GdPrv', max_length=6, verbose_name='Паркан, огорожа'),
        ),
        migrations.AlterField(
            model_name='house',
            name='GarageType',
            field=models.CharField(choices=[('2Types', 'Більше чим 1 тип гаражу'), ('Attchd', 'Гараж приєднаний до будинку'), ('Basment', 'Гараж у фундаменті, підземний'), ('BuiltIn', 'Гараж - частина будинку, має кімнату зверху'), ('CarPort', 'Навіс для машини'), ('Detchd', 'Гараж окремо від будинку'), ('NA', 'Немає гаражу')], default='NA', max_length=20, verbose_name='Гараж'),
        ),
        migrations.AlterField(
            model_name='house',
            name='GrLivArea',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Уся житлова площа, кв.м'),
        ),
        migrations.AlterField(
            model_name='house',
            name='TotRmsAbvGrd',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Кількість кімнат'),
        ),
        migrations.AlterField(
            model_name='house',
            name='cable_digital_tv',
            field=models.BooleanField(verbose_name='Кабельне або супутникове ТБ'),
        ),
        migrations.AlterField(
            model_name='house',
            name='currency',
            field=models.CharField(choices=[('UAH', 'грн.'), ('USD', 'USD')], default='USD', max_length=3, verbose_name='Валюта'),
        ),
        migrations.AlterField(
            model_name='house',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Ціна, $'),
        ),
    ]
