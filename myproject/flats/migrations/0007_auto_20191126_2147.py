# Generated by Django 2.2.7 on 2019-11-26 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0006_auto_20191126_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='address',
        ),
        migrations.AddField(
            model_name='offer',
            name='flat',
            field=models.CharField(blank=True, help_text="Не показується на сайті. Необов'язкове поле.'", max_length=3, null=True, verbose_name='Номер квартири'),
        ),
        migrations.AddField(
            model_name='offer',
            name='house',
            field=models.CharField(default='', max_length=10, verbose_name='Номер будинку'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='notes',
            field=models.TextField(default='', max_length=1000, verbose_name='Примітки для службового користування'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='street',
            field=models.CharField(default='', max_length=255, verbose_name='Вулиця'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='offer',
            name='district',
            field=models.CharField(choices=[('Райони', (('700-richchia', '700-річчя'), ('Vantazhnyi port', 'Вантажний порт'), ('Vodokanal-Nevskoho', 'Водоканал-Невського'), ('Dakhnivka', 'Дахнівка'), ('Dniprovskyi', 'Дніпровський'), ('Zaliznychnyi vokzal', 'Залізничний вокзал'), ('Zelena', 'Зелена'), ('k-t Myr', 'к-т Мир'), ('Kazbet', 'Казбет'), ('Litak', 'Літак'), ('Lunacharskyi', 'Луначарський'), ('Mytnytsia', 'Митниця'), ('Mytnytsia-richport', 'Митниця-річпорт'), ('Mytnytsia-tsentr', 'Митниця-центр'), ('PZR', 'ПЗР'), ('Prydniprovskyi', 'Придніпровський'), ('Piatykhatky', 'Пятихатки'), ('Raion D', 'Район Д'), ('Siedova', 'Сєдова'), ('Sosnivka', 'Соснівка'), ('Sosnivskyi', 'Соснівський'), ('Khimselyshche', 'Хімселище'), ('Tsentr', 'Центр'), ('Shkilna', 'Шкільна'), ('Yabluchnyi', 'Яблучний'))), ('Передмістя', (('Biloziria', "Білозір'я"), ('Heronymivka', 'Геронимівка'), ('Orshanets', 'Оршанець'), ('Ruska Poliana', 'Руська Поляна'), ('Chervona Sloboda', 'Червона Слобода'))), ('Села', (('Yelyzavetovka', 'Єлизаветовка'), ('Irdyn', 'Ірдинь'), ('Baibuzy', 'Байбузи'), ('Berezniaky', 'Березняки'), ('Budyshche', 'Будище'), ('Buzukiv', 'Бузуків'), ('Verhuny', 'Вергуни'), ('Dubiivka', 'Дубіївка'), ('Dumantsi', 'Думанці'), ('Kumeiky', 'Кумейки'), ('Lesky', 'Леськи'), ('Lozivok', 'Лозівок'), ('Moshny', 'Мошни'), ('Moshnohiria', "Мошногір'я"), ('Nechaivka', 'Нечаївка'), ('Novoselivka', 'Новоселівка'), ('Pervomaiske', 'Первомайське'), ('Sahunivka', 'Сагунівка'), ('Svitanok', 'Світанок'), ('Svydivok', 'Свидівок'), ('Sokyrno', 'Сокирно'), ('Sofiivka', 'Софіївка'), ('Stepanky', 'Степанки'), ('Tubiltsi', 'Тубільці'), ('Khatsky', 'Хацьки'), ('Khreshchatyk', 'Хрещатик'), ('Khudiaky', 'Худяки'), ('Khutory', 'Хутори'), ('Chorniavka', 'Чорнявка'), ('Shelepukhy', 'Шелепухи'), ('Yasnoziria', "Яснозір'я")))], max_length=30, verbose_name='Район'),
        ),
    ]
