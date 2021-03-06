# Generated by Django 2.2.7 on 2020-02-01 15:23

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import realtor.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geometry', django.contrib.gis.db.models.fields.PointField(extent=(31.44, 49.217, 32.47, 49.68), help_text='<em>Просто поставте маркер на карту</em>', srid=4326, verbose_name='Місце на мапі')),
                ('name', models.CharField(max_length=255, verbose_name='Назва агенції')),
                ('phone1', models.CharField(help_text='міжнародний формат, +38067XXXYYZZ', max_length=13, verbose_name='Телефон основний')),
                ('phone2', models.CharField(help_text='міжнародний формат, +38067XXXYYZZ', max_length=13, verbose_name='Телефон додатковий')),
                ('body', models.TextField(help_text='<em>До 2000 символів</em>', max_length=2000, verbose_name='Про Агенція')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адреса')),
                ('slug', models.SlugField(default='', editable=False, max_length=100)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('num_visits', models.PositiveIntegerField(default=0)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='media', verbose_name='Логотип')),
                ('created_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Власник сторінки')),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='StatisticUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit_offers', models.PositiveSmallIntegerField(default=1, verbose_name='Ліміт оголошень, штук')),
                ('offers', models.PositiveSmallIntegerField(default=0, verbose_name="Об'єктів на продаж")),
                ('in_archive', models.PositiveSmallIntegerField(default=0, verbose_name="Об'єктів в архіві")),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='Realtor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(help_text='міжнародний формат, +38067XXXYYZZ', max_length=13, verbose_name='Телефон основний')),
                ('start_year', models.CharField(max_length=4, verbose_name='Рік початку роботи ріелтором')),
                ('bio', models.TextField(blank=True, help_text='<em>все, що вважаєте за потрібне про себе, свою фірму до 1000 знаків</em>', max_length=1000, null=True, verbose_name='Подробиці про ріелтора')),
                ('num_visits', models.PositiveIntegerField(default=0)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=realtor.models.Realtor.user_directory_path, verbose_name='Фото ріелтора')),
                ('agency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='realtors', to='realtor.Agency', verbose_name='Агенція')),
                ('created_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Власник профілю')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.PositiveIntegerField(verbose_name='Сума оплати')),
                ('currency', models.CharField(choices=[('UAH', 'UAH'), ('USD', 'USD'), ('EUR', 'EUR')], default='EUR', max_length=3, verbose_name='Валюта')),
                ('pay_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
