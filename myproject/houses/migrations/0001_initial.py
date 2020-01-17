# Generated by Django 2.2.7 on 2020-01-17 07:15

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import houses.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geometry', django.contrib.gis.db.models.fields.PointField(extent=(31.44, 49.217, 32.47, 49.68), help_text='<em>Просто поставте маркер на карту</em>', srid=4326, verbose_name='Місце на мапі')),
                ('type_offer', models.CharField(choices=[('SALE', 'Продаж'), ('RENT', 'Оренда довгострокова')], default='SALE', max_length=50, verbose_name='Тип оголошення')),
                ('title', models.CharField(help_text='70 знаків', max_length=70, verbose_name='Заголовок')),
                ('price', models.PositiveIntegerField(verbose_name='Ціна')),
                ('currency', models.CharField(choices=[('UAH', 'грн.'), ('USD', 'USD')], default='USD', max_length=3, verbose_name='Валюта')),
                ('MSSubClass', models.CharField(choices=[('20', '1-ПОВЕРХ 2000 І НОВІШИЙ ВСІ СТИЛІ'), ('30', '1-ПОВЕРХ 1999 І СТАРІШИЙ'), ('40', '1-1/2 ПОВЕРХ МАНСАРДА НЕЗАКІНЧЕНИЙ ВСІ РОКИ'), ('50', '1-1/2 ПОВЕРХ МАНСАРДА ЗАКІНЧЕНИЙ ВСІ РОКИ'), ('60', '2-ПОВЕРХ 2000 І НОВІШИЙ'), ('70', '2-ПОВЕРХ 1999 І СТАРІШИЙ'), ('75', '2-1/2 ПОВЕРХ ВСІ РОКИ'), ('80', 'БАГАТОРІВНЕВИЙ'), ('90', 'КІЛЬКАПОВЕРХОВИЙ З ФОЙЕ'), ('110', 'ДУПЛЕКС, ТАУНХАУС - УСІ СТИЛІ 2010 І НОВІШІ'), ('120', '1-ПОВЕРХ ТИПОВИЙ РАДЯНСЬКИЙ ПРОЕКТ - 1960 І НОВІШІ'), ('150', "НА 2 СІМ'Ї - ТИПОВИЙ РАДЯНСЬКИЙ ПРОЕКТ")], default='20', help_text='Визначає тип житла, що бере участь у продажу', max_length=3, verbose_name="Тип об'єкта")),
                ('YearBuilt', models.CharField(blank=True, max_length=4, null=True, verbose_name='Рік будівництва')),
                ('YearRenovation', models.CharField(blank=True, max_length=4, null=True, verbose_name='Рік останньої реновації')),
                ('Architecture', models.CharField(choices=[('empire', 'ампір'), ('classicism', 'класицизм'), ('chalet', 'шале'), ('constructivism', 'конструктивізм'), ('hi-tech', 'хай-тек'), ('renaissance', 'ренесанс'), ('baroque', 'барокко'), ('modern', 'модерн'), ('other', 'інший')], default='classicism', max_length=20, verbose_name='Архітектурний стиль')),
                ('MSZoning', models.CharField(choices=[('A', 'СІЛЬСЬКЕ ГОСПОДАРСТВО'), ('C', 'КОМЕРЦІЙНА'), ('FV', 'ПРИМІСЬКА'), ('I', 'ПРОМИСЛОВА'), ('RH', 'ВИСОКА ЩІЛЬНІСТЬ ЗАБУДОВИ'), ('RL', 'НИЗЬКА ЩІЛЬНІСТЬ ЗАБУДОВИ'), ('RP', 'КОТЕДЖНЕ МІСТЕЧКО З НИЗЬКОЮ ЩІЛЬНІСТЮ ЗАБУДОВИ'), ('RM', 'СЕРЕДНЯ ЩІЛЬНІСТЬ ЗАБУДОВИ')], default='A', help_text='Визначає загальну класифікацію зонування продажу', max_length=3, verbose_name='Зонування')),
                ('LotFrontage', models.PositiveIntegerField(blank=True, help_text='Довжина вулиці в метрах, де приєднана власність', null=True, verbose_name='Лицьова сторона власності, метрів')),
                ('LotShape', models.CharField(choices=[('Reg', 'Правильна форма'), ('IR1', 'Майже правильна'), ('IR2', 'Помірно неправильна'), ('IR3', 'Дуже неправильна')], default='Reg', max_length=3, verbose_name='Форма земельної ділянки')),
                ('LandContour', models.CharField(choices=[('Lvl', 'Все в одному рівні, плоска ділянка'), ('Bnk', 'Швидкий і значний підйом з вулиці в будівлю'), ('HLS', 'Значний нахил ділянки з боку в бік'), ('Low', 'Нижче рівня вулиці, улоговина'), ('Slp', 'Помірний рівномірний схил')], default='Lvl', max_length=3, verbose_name='Плоскість власності')),
                ('Walls', models.CharField(choices=[('SilBrick', 'Силікатна цегла'), ('RedBrick', 'Червона цегла'), ('CerBlock', 'Керамоблок'), ('Wood', "Дерев'яний'"), ('CindBlock', 'Шлакоблочний'), ('AirConcrete', 'Газоблок'), ('SIP', 'СІП панель'), ('Other', 'Інше')], default='Other', max_length=20, verbose_name='Основний матеріал стін')),
                ('RoofMatl', models.CharField(choices=[('MetalTile', 'металочерепиця'), ('Metal', 'Метал'), ('ClyTile', 'керамічна черепиця'), ('BitumTile', 'Бітумна черепиця'), ('CemTile', 'Пісчано-цементна черепиця'), ('Shale', 'Сланцеве покриття'), ('Slate', 'Шифер'), ('Other', 'Інше')], default='Other', max_length=20, verbose_name='Матеріал даху')),
                ('Exterior', models.CharField(blank=True, max_length=160, null=True, verbose_name='Матеріали фінішної обробки фасаду')),
                ('ExterCond', models.CharField(choices=[('Ex', 'Преміум'), ('Gd', 'Добрий'), ('TA', 'Середній'), ('Fa', 'Мінімально достатній'), ('Po', 'Бідний')], default='TA', max_length=2, verbose_name="Загальний стан екстер'єру будинку")),
                ('Foundation', models.CharField(blank=True, max_length=255, null=True, verbose_name='Матеріал, тип, глибина, стан фундаменту')),
                ('FirstFloor', models.CharField(blank=True, max_length=20, null=True, verbose_name='Загальна площа 1 поверху, кв.м')),
                ('SecondFloor', models.CharField(blank=True, max_length=20, null=True, verbose_name='Площа 2-го поверху')),
                ('LowQualFinSF', models.CharField(blank=True, max_length=20, null=True, verbose_name="Площа де ремонт незакінчено або обробка інтер'єру низької якості, усі поверхи, кв.м")),
                ('GrLivArea', models.CharField(blank=True, max_length=20, null=True, verbose_name='Уся житлова площа над рівнем землі, кв.м')),
                ('Bedroom', models.CharField(blank=True, max_length=2, null=True, verbose_name='Кількість спалень над рівнем землі')),
                ('TotRmsAbvGrd', models.CharField(blank=True, max_length=2, null=True, verbose_name='Кількість кімнат над рівнем землі')),
                ('Kitchen', models.CharField(choices=[('Ex', 'Преміум'), ('Gd', 'Добрий'), ('TA', 'Середній'), ('Fa', 'Мінімально достатній'), ('Po', 'Бідний')], default='TA', max_length=2, verbose_name='Загальний стан кухні')),
                ('Bathroom', models.CharField(choices=[('different', 'Роздільний'), ('adjacent', 'Суміжний'), ('two_and_more', '2 і більше'), ('no_bathrooms', 'Санвузол відсутній')], default='different', max_length=20, verbose_name='Санвузол')),
                ('Repair', models.CharField(choices=[('authors_project', 'Авторський проект'), ('european_repair', 'Євроремонт'), ('cosmetical_repair', 'Косметичний ремонт'), ('life_condition', 'Житловий стан'), ('after_construction', 'Після будівельників'), ('for_clean_processing', 'під чистову обробку'), ('emergency_condition', 'Аварійний стан')], default='life_condition', max_length=20, verbose_name="Ремонт інтер'єру")),
                ('Heating', models.CharField(choices=[('centralize', 'Централізоване'), ('own_boiler_room', 'Власна котельня'), ('individual_gas', 'Індивідуальне газове'), ('individual_electricity', 'Індивідуальне електричне'), ('hard_fuel', 'Твердопаливне'), ('heat_pump', 'Тепловий насос'), ('combination', 'Комбіноване'), ('other', 'Інше')], default='other', max_length=20, verbose_name='Опалення')),
                ('GarageType', models.CharField(choices=[('2Types', 'Більше чим 1 тип гаражу'), ('Attchd', 'Гараж приєднаний до будинку'), ('Basment', 'Гараж у фундаменті, підземний'), ('BuiltIn', 'Гараж - частина будинку, має кімнату зверху'), ('CarPort', 'Навіс для машини'), ('Detchd', 'Гараж окремо від будинку'), ('NA', 'Немає гаражу')], default='NA', max_length=20, verbose_name='Тип гаражу')),
                ('GarageYrBlt', models.CharField(blank=True, max_length=4, null=True, verbose_name='Рік побудови гаражу')),
                ('GarageFinish', models.CharField(choices=[('Fin', 'Закінчена, чистова'), ('Rfn', 'Чорнова, часткова'), ('Unf', 'Незакінчена'), ('NA', 'Немає гаражу')], default='NA', max_length=3, verbose_name="Інтер'єр, обробка")),
                ('GarageCars', models.CharField(blank=True, max_length=1, null=True, verbose_name='Розмір гаражу, кількість машин')),
                ('GarageArea', models.CharField(blank=True, max_length=7, null=True, verbose_name='Площа гаражу, кв.м')),
                ('GarageCond', models.CharField(choices=[('Ex', 'Преміум'), ('Gd', 'Добре'), ('TA', 'Типова/середня'), ('Fa', 'Достатньо чисто'), ('Po', 'Бідно'), ('NA', 'Немає гаражу')], default='NA', max_length=2, verbose_name='Загальний стан гаражу')),
                ('PoolArea', models.CharField(blank=True, max_length=7, null=True, verbose_name='Загальна площа басейну, кв.м')),
                ('PoolQC', models.CharField(choices=[('Ex', 'Преміум'), ('Gd', 'Добре'), ('TA', 'Типова/середня'), ('Fa', 'Достатньо чисто'), ('Po', 'Бідно'), ('NA', 'Немає басейну')], default='NA', max_length=2, verbose_name='Загальний стан басейну')),
                ('Fence', models.CharField(choices=[('GdPrv', 'Добре захищена приватність'), ('MnPrv', 'Мінімальна приватність'), ('BadPrv', 'Погано захищена приватність'), ('NA', 'Немає огорожі')], default='NA', max_length=6, verbose_name='Якість паркану, огорожі')),
                ('Fireplace', models.CharField(blank=True, max_length=160, null=True, verbose_name='Камін, тип, якість, стан')),
                ('body', models.TextField(help_text='<em>до 4000 знаків</em>', max_length=4000, verbose_name='Опис')),
                ('agree_price', models.BooleanField(verbose_name='Договірна')),
                ('no_commission', models.BooleanField(verbose_name='Без комісії')),
                ('exchange', models.BooleanField(verbose_name='Можливість обміну')),
                ('collaboration', models.BooleanField(verbose_name='Готовий співпрацювати з ріелторами')),
                ('image1', models.ImageField(blank=True, null=True, upload_to=houses.models.House.user_directory_path, verbose_name='Світлина 1')),
                ('image2', models.ImageField(blank=True, null=True, upload_to=houses.models.House.user_directory_path, verbose_name='Світлина 2')),
                ('image3', models.ImageField(blank=True, null=True, upload_to=houses.models.House.user_directory_path, verbose_name='Світлина 3')),
                ('image4', models.ImageField(blank=True, null=True, upload_to=houses.models.House.user_directory_path, verbose_name='Світлина 4')),
                ('image5', models.ImageField(blank=True, null=True, upload_to=houses.models.House.user_directory_path, verbose_name='Світлина 5')),
                ('image6', models.ImageField(blank=True, null=True, upload_to=houses.models.House.user_directory_path, verbose_name='Світлина 6')),
                ('image7', models.ImageField(blank=True, null=True, upload_to=houses.models.House.user_directory_path, verbose_name='Світлина 7')),
                ('image8', models.ImageField(blank=True, null=True, upload_to=houses.models.House.user_directory_path, verbose_name='Світлина 8')),
                ('image9', models.ImageField(blank=True, null=True, upload_to=houses.models.House.user_directory_path, verbose_name='Світлина 9')),
                ('plate', models.BooleanField(verbose_name='Плита')),
                ('cooking_plate', models.BooleanField(verbose_name='Варочна поверхня')),
                ('oven', models.BooleanField(verbose_name='Духова шафа')),
                ('microwave', models.BooleanField(verbose_name='Мікрохвильова піч')),
                ('refrigerator', models.BooleanField(verbose_name='Холодильник')),
                ('dishwashers', models.BooleanField(verbose_name='Посудомийна машина')),
                ('washing_machine', models.BooleanField(verbose_name='Пральна машина')),
                ('dryer', models.BooleanField(verbose_name='Сушильна машина')),
                ('wi_fi', models.BooleanField(verbose_name='WI-FI')),
                ('high_speed_internet', models.BooleanField(verbose_name='Швидкісний інтернет')),
                ('tv', models.BooleanField(verbose_name='Телевізор')),
                ('cable_digital_tv', models.BooleanField(verbose_name='Кабельнеб цифрове ТБ')),
                ('satellite_tv', models.BooleanField(verbose_name='Супутникове ТБ')),
                ('air_conditioning', models.BooleanField(verbose_name='Кондиціонер')),
                ('floor_heating', models.BooleanField(verbose_name='Підігрів підлоги')),
                ('bath', models.BooleanField(verbose_name='Ванна')),
                ('shower', models.BooleanField(verbose_name='Душ')),
                ('kitchen_furniture', models.BooleanField(verbose_name='Меблі на кухні')),
                ('wardrobe', models.BooleanField(verbose_name='Гардероб')),
                ('balcony', models.BooleanField(verbose_name='Балкон, лоджія')),
                ('terrace', models.BooleanField(verbose_name='Тераса')),
                ('panoramic_windows', models.BooleanField(verbose_name='Панорамні вікна')),
                ('grid_on_the_windows', models.BooleanField(verbose_name='Грати на вікнах')),
                ('alarms', models.BooleanField(verbose_name='Сигналізація')),
                ('fire_alarm', models.BooleanField(verbose_name='Пожежна сигналізація')),
                ('video_surveillance', models.BooleanField(verbose_name='Відеоспостереження')),
                ('protection_of_the_territory', models.BooleanField(verbose_name='Охорона території')),
                ('elevator', models.BooleanField(verbose_name='Ліфт')),
                ('tennis_court', models.BooleanField(default=False, verbose_name='Тенісний корт')),
                ('pantry', models.BooleanField(verbose_name='Сарай більше 50 кв.м')),
                ('smart_home_technology', models.BooleanField(verbose_name='Технологія "розумний будинок"')),
                ('autonomous_generator', models.BooleanField(verbose_name='Автономний електрогенератор')),
                ('gas', models.BooleanField(verbose_name='Газ')),
                ('central_water_supply', models.BooleanField(verbose_name='Центральний водопровід')),
                ('well', models.BooleanField(verbose_name='Скважина')),
                ('electricity', models.BooleanField(verbose_name='Електрика')),
                ('central_sewerage', models.BooleanField(verbose_name='Центральна каналізація')),
                ('septic_tank', models.BooleanField(verbose_name='Каналізація септик')),
                ('removal_of_waste', models.BooleanField(verbose_name='Вивіз відходів')),
                ('asphalt_road', models.BooleanField(verbose_name='Асфальтована дорога')),
                ('kindergarten', models.BooleanField(verbose_name='Дитячий садок')),
                ('school', models.BooleanField(verbose_name='Школа')),
                ('the_pump_room', models.BooleanField(verbose_name='Бювет')),
                ('transportation_stop', models.BooleanField(verbose_name='Зупинка транспорту')),
                ('market', models.BooleanField(verbose_name='Ринок')),
                ('shop_kiosk', models.BooleanField(verbose_name='Магазин, кіоск')),
                ('supermarket_mall', models.BooleanField(verbose_name='Супермаркет, ТРЦ')),
                ('park_green_area', models.BooleanField(verbose_name='Парк, зелена зона')),
                ('playground', models.BooleanField(verbose_name='Дитячий майданчик')),
                ('pharmacy', models.BooleanField(verbose_name='Аптека')),
                ('hospital_clinic', models.BooleanField(verbose_name='Лікарня, поліклініка')),
                ('city_center', models.BooleanField(verbose_name='Центр міста')),
                ('restaurant_cafe', models.BooleanField(verbose_name='Ресторан, кафе')),
                ('cinema_theater', models.BooleanField(verbose_name='Кінотеатр, театр')),
                ('post_office', models.BooleanField(verbose_name='Відділення пошти')),
                ('bank_branch_ATM', models.BooleanField(verbose_name='Відділення банку, банкомат')),
                ('bus_station', models.BooleanField(verbose_name='Автовокзал')),
                ('railway_station', models.BooleanField(verbose_name='Залізнична станція')),
                ('river', models.BooleanField(verbose_name='Річка')),
                ('reservoir', models.BooleanField(verbose_name='Водосховище')),
                ('lake', models.BooleanField(verbose_name='Озеро')),
                ('hills', models.BooleanField(verbose_name='Пагорби')),
                ('mountains', models.BooleanField(verbose_name='Гори')),
                ('park', models.BooleanField(verbose_name='Парк')),
                ('forest', models.BooleanField(verbose_name='Ліс')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адреса')),
                ('slug', models.SlugField(default='', editable=False, max_length=200)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('num_visits', models.PositiveIntegerField(default=0)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='houses', to=settings.AUTH_USER_MODEL, verbose_name='Власник оголошення')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
    ]
