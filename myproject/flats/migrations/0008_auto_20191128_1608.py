# Generated by Django 2.2.7 on 2019-11-28 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import flats.models


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0007_auto_20191126_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='image',
        ),
        migrations.AddField(
            model_name='offer',
            name='contract',
            field=models.FileField(null=True, upload_to=flats.models.Offer.user_directory_path, verbose_name='Файл договору на Продаж'),
        ),
        migrations.AddField(
            model_name='offer',
            name='image1',
            field=models.ImageField(null=True, upload_to=flats.models.Offer.user_directory_path, verbose_name='Фото 1'),
        ),
        migrations.AddField(
            model_name='offer',
            name='image2',
            field=models.ImageField(null=True, upload_to=flats.models.Offer.user_directory_path, verbose_name='Фото 2'),
        ),
        migrations.AddField(
            model_name='offer',
            name='image3',
            field=models.ImageField(null=True, upload_to=flats.models.Offer.user_directory_path, verbose_name='Фото 3'),
        ),
        migrations.AddField(
            model_name='offer',
            name='image4',
            field=models.ImageField(null=True, upload_to=flats.models.Offer.user_directory_path, verbose_name='Фото 4'),
        ),
        migrations.AddField(
            model_name='offer',
            name='image5',
            field=models.ImageField(null=True, upload_to=flats.models.Offer.user_directory_path, verbose_name='Фото 5'),
        ),
        migrations.AddField(
            model_name='offer',
            name='image6',
            field=models.ImageField(null=True, upload_to=flats.models.Offer.user_directory_path, verbose_name='Фото 6'),
        ),
        migrations.AddField(
            model_name='offer',
            name='image7',
            field=models.ImageField(null=True, upload_to=flats.models.Offer.user_directory_path, verbose_name='Фото 7'),
        ),
        migrations.AddField(
            model_name='offer',
            name='image8',
            field=models.ImageField(null=True, upload_to=flats.models.Offer.user_directory_path, verbose_name='Фото 8'),
        ),
        migrations.AddField(
            model_name='offer',
            name='image9',
            field=models.ImageField(null=True, upload_to=flats.models.Offer.user_directory_path, verbose_name='Фото 9'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='area',
            field=models.PositiveSmallIntegerField(verbose_name='Загальна площа, кв.м'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='bathroom',
            field=models.CharField(choices=[('None', 'Виберіть санвузол'), ('different', 'Роздільний'), ('adjacent', 'Суміжний'), ('two_and_more', '2 і більше'), ('no_bathrooms', 'Санвузол відсутній')], max_length=14, verbose_name='Санвузол'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='building',
            field=models.CharField(choices=[('None', 'Виберіть тип будинку'), ('royal', 'Царський будинок'), ('stalin', 'Сталінка'), ('hruschov', 'Хрущовка'), ('czech', 'Чешка'), ('guest', 'Гостинка'), ('sovmin', 'Совмін'), ('hostel', 'Гуртожиток'), ('90', 'Житловий фонд 80-90'), ('2000', 'Житловий фонд 91-2000'), ('2010', 'Житловий фонд 2001-2010'), ('2019', 'Житловий фонд від 2011'), ('constraction', 'На етапі будівництва')], max_length=12, verbose_name='Тип будинку'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flats', to=settings.AUTH_USER_MODEL, verbose_name='Власник оголошення'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='floor',
            field=models.PositiveSmallIntegerField(verbose_name='Поверх'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='house',
            field=models.CharField(max_length=6, verbose_name='Номер будинку'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='kitchen',
            field=models.PositiveSmallIntegerField(verbose_name='Кухня площа, кв.м'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='pantry',
            field=models.BooleanField(verbose_name='Госп. приміщення, комора'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='planning',
            field=models.CharField(choices=[('None', 'Виберіть планування'), ('adjacent', 'Суміжна, прохідна'), ('different', 'Роздільна'), ('studio', 'Студія'), ('penthouse', 'Пентхаус'), ('multilevel', 'Багаторівнева'), ('small_family', 'Малосімейка, гостинка'), ('smart_flat', 'Смарт-квартира'), ('free_planning', 'Вільне планування'), ('two_sides', 'Двостороння')], default='brick', max_length=14, verbose_name='Планування квартири'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='offer',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Ціна'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='repair',
            field=models.CharField(choices=[('None', 'Виберіть стан ремонту'), ('authors_project', 'Авторський проект'), ('european_repair', 'Євроремонт'), ('cosmetical_repair', 'Косметичний ремонт'), ('life_condition', 'Житловий стан'), ('after_construction', 'Після будівельників'), ('for_clean_processing', 'під чистову обробку'), ('emergency_condition', 'Аварійний стан')], max_length=24, verbose_name='Ремонт'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='rooms',
            field=models.PositiveSmallIntegerField(default=3, verbose_name='Кількість кімнат'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='offer',
            name='sold_true',
            field=models.CharField(choices=[('yes', 'Так'), ('no', 'Ні')], default='no', help_text='Якщо об\'єкт під задатком виберіть "Так".\n              Картка об\'єкта буде знята з пошуку.', max_length=3, verbose_name="ОБ'ЄКТ під ЗАДАТКОМ?"),
        ),
        migrations.AlterField(
            model_name='offer',
            name='street',
            field=models.CharField(max_length=55, verbose_name='Вулиця, провулок, бульвар'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='total_floor',
            field=models.PositiveSmallIntegerField(verbose_name='Поверхів'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='walls',
            field=models.CharField(choices=[('None', 'Виберіть стіни'), ('brick', 'Цегляний'), ('panel', 'Панельний'), ('monolit', 'Монолітний'), ('wood', "Дерев'яний'"), ('cinder_block', 'Шлакоблочний'), ('air_concrete', 'Газоблок'), ('sip', 'СІП панель'), ('other', 'Інше')], max_length=10, verbose_name='Матеріал стін'),
        ),
    ]
