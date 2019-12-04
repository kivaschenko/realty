# Generated by Django 2.2.7 on 2019-12-02 22:07

from django.conf import settings
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
            name='Realtor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(help_text='міжнародний формат, +38067XXXYYZZ', max_length=13, verbose_name='Телефон основний')),
                ('phone2', models.CharField(blank=True, help_text='міжнародний формат, +38067XXXYYZZ', max_length=13, verbose_name='Телефон додатковий')),
                ('start_year', models.CharField(max_length=4, verbose_name='Рік початку роботи ріелтором')),
                ('agensy', models.CharField(blank=True, help_text='назва компанії, в якії працюєте', max_length=50, null=True, verbose_name='Агенство, компанія')),
                ('bio', models.TextField(blank=True, help_text='все, що вважаєте за потрібне про себе, свою фірму до 1000 знаків', max_length=1000, null=True, verbose_name='Подробиці про ріелтора')),
                ('address', models.CharField(max_length=155, verbose_name='Адреса офісу')),
                ('district', models.CharField(choices=[('Райони', (('700-richchia', '700-річчя'), ('Vantazhnyi port', 'Вантажний порт'), ('Vodokanal-Nevskoho', 'Водоканал-Невського'), ('Dakhnivka', 'Дахнівка'), ('Dniprovskyi', 'Дніпровський'), ('Zaliznychnyi vokzal', 'Залізничний вокзал'), ('Zelena', 'Зелена'), ('k-t Myr', 'к-т Мир'), ('Kazbet', 'Казбет'), ('Litak', 'Літак'), ('Lunacharskyi', 'Луначарський'), ('Mytnytsia', 'Митниця'), ('Mytnytsia-richport', 'Митниця-річпорт'), ('Mytnytsia-tsentr', 'Митниця-центр'), ('PZR', 'ПЗР'), ('Prydniprovskyi', 'Придніпровський'), ('Piatykhatky', 'Пятихатки'), ('Raion D', 'Район Д'), ('Siedova', 'Сєдова'), ('Sosnivka', 'Соснівка'), ('Sosnivskyi', 'Соснівський'), ('Khimselyshche', 'Хімселище'), ('Tsentr', 'Центр'), ('Shkilna', 'Шкільна'), ('Yabluchnyi', 'Яблучний'))), ('Передмістя', (('Biloziria', "Білозір'я"), ('Heronymivka', 'Геронимівка'), ('Orshanets', 'Оршанець'), ('Ruska Poliana', 'Руська Поляна'), ('Chervona Sloboda', 'Червона Слобода'))), ('Села', (('Yelyzavetovka', 'Єлизаветовка'), ('Irdyn', 'Ірдинь'), ('Baibuzy', 'Байбузи'), ('Berezniaky', 'Березняки'), ('Budyshche', 'Будище'), ('Buzukiv', 'Бузуків'), ('Verhuny', 'Вергуни'), ('Dubiivka', 'Дубіївка'), ('Dumantsi', 'Думанці'), ('Kumeiky', 'Кумейки'), ('Lesky', 'Леськи'), ('Lozivok', 'Лозівок'), ('Moshny', 'Мошни'), ('Moshnohiria', "Мошногір'я"), ('Nechaivka', 'Нечаївка'), ('Novoselivka', 'Новоселівка'), ('Pervomaiske', 'Первомайське'), ('Sahunivka', 'Сагунівка'), ('Svitanok', 'Світанок'), ('Svydivok', 'Свидівок'), ('Sokyrno', 'Сокирно'), ('Sofiivka', 'Софіївка'), ('Stepanky', 'Степанки'), ('Tubiltsi', 'Тубільці'), ('Khatsky', 'Хацьки'), ('Khreshchatyk', 'Хрещатик'), ('Khudiaky', 'Худяки'), ('Khutory', 'Хутори'), ('Chorniavka', 'Чорнявка'), ('Shelepukhy', 'Шелепухи'), ('Yasnoziria', "Яснозір'я")))], max_length=30, verbose_name='Район офісу')),
                ('num_visits', models.PositiveIntegerField(default=0)),
                ('rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3, verbose_name='Рейтинг')),
                ('offers', models.PositiveSmallIntegerField(default=0, verbose_name="Об'єктів на продаж")),
                ('in_archive', models.PositiveSmallIntegerField(default=0, verbose_name="Об'єктів в архіві")),
                ('image1', models.ImageField(blank=True, null=True, upload_to=realtor.models.Realtor.user_directory_path, verbose_name='Фoto сертифікату 1')),
                ('image2', models.ImageField(blank=True, null=True, upload_to=realtor.models.Realtor.user_directory_path, verbose_name='Фото сертифікату 2')),
                ('image3', models.ImageField(blank=True, null=True, upload_to=realtor.models.Realtor.user_directory_path, verbose_name='Фото сертифікату 3')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=realtor.models.Realtor.user_directory_path, verbose_name='Фото ріелтора')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Власник профілю')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=1, verbose_name='Загальне враження від співпраці')),
                ('rating', models.PositiveSmallIntegerField(default=0)),
                ('message', models.TextField(help_text='до 2000 знаків', max_length=2000, verbose_name='Відгук')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('realtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realtor.Realtor')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Дякую за відгук', max_length=50, verbose_name='Заголовок')),
                ('message', models.TextField(help_text='до 2000 знаків', max_length=2000, verbose_name='Відповідь')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('review', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='realtor.Review')),
            ],
        ),
    ]
