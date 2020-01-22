import datetime
from translitua import translit
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim

geolocator = Nominatim(timeout=7, user_agent='houses')


class House(models.Model):
    address = models.CharField(max_length=255)
    geometry = geomodels.PointField(verbose_name='Місце на мапі',
             extent=(31.44, 49.217, 32.47, 49.68),
             help_text='<em>Просто поставте маркер на карту</em>')
    @property
    def lat_lng(self):
        return list(getattr(self.geometry, 'coords', [])[::-1])
    # GENERAL FIELDS
    type_offer = models.CharField(max_length=50, verbose_name="Тип оголошення",
                choices=(
                    ('sale', 'Продаж'),
                    ('rent', 'Оренда довгострокова')),
                default='SALE')
    title = models.CharField(max_length=70, verbose_name='Заголовок',
          help_text='70 знаків', blank=False)
    price = models.PositiveIntegerField(verbose_name='Ціна')
    currency = models.CharField(verbose_name='Валюта', max_length=3,
             choices=(('UAH', 'грн.'), ('USD', 'USD')), blank=False,
             default='USD',)

    # COLLABORATION
    agree_price = models.BooleanField('Договірна')
    no_commission = models.BooleanField(verbose_name='Без комісії')
    exchange = models.BooleanField(verbose_name='Можливість обміну')
    collaboration = models.BooleanField(
        verbose_name='Готовий співпрацювати з ріелторами')
    # SAVING MEDIA FILES
    def user_directory_path(instance, filename):
        img_path = 'user_{0}/{1}'.format(instance.created_by.id, filename)
        return img_path
    image1 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Світлина 1', null=True, blank=True)
    image2 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Світлина 2', null=True, blank=True)
    image3 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Світлина 3', null=True, blank=True)
    image4 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Світлина 4', null=True, blank=True)
    image5 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Світлина 5', null=True, blank=True)
    image6 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Світлина 6', null=True, blank=True)
    image7 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Світлина 7', null=True, blank=True)
    image8 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Світлина 8', null=True, blank=True)
    image9 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Світлина 9', null=True, blank=True)
    # MSSubClass: Identifies the type of dwelling involved in the sale.
    MSSubClass = models.CharField(max_length=3,
                choices=(
                    ('20',    '1-ПОВЕРХ 2000 І НОВІШИЙ ВСІ СТИЛІ'),
                    ('30',    '1-ПОВЕРХ 1999 І СТАРІШИЙ'),
                    ('40',	'1-1/2 ПОВЕРХ МАНСАРДА НЕЗАКІНЧЕНИЙ ВСІ РОКИ'),
                    ('50',	'1-1/2 ПОВЕРХ МАНСАРДА ЗАКІНЧЕНИЙ ВСІ РОКИ'),
                    ('60',	'2-ПОВЕРХ 2000 І НОВІШИЙ'),
                    ('70',	'2-ПОВЕРХ 1999 І СТАРІШИЙ'),
                    ('75',	'2-1/2 ПОВЕРХ ВСІ РОКИ'),
                    ('80',	'БАГАТОРІВНЕВИЙ'),
                    ('90',	'КІЛЬКАПОВЕРХОВИЙ З ФОЙЕ'),
                    ('110',	'ДУПЛЕКС, ТАУНХАУС - УСІ СТИЛІ 2010 І НОВІШІ'),
                    ('120',	'1-ПОВЕРХ ТИПОВИЙ РАДЯНСЬКИЙ ПРОЕКТ - 1960 І НОВІШІ'),
                    ('150',	"НА 2 СІМ'Ї - ТИПОВИЙ РАДЯНСЬКИЙ ПРОЕКТ")),
                verbose_name="Тип об'єкта",
                help_text='Визначає тип житла, що бере участь у продажу',
                default='20')
    YearBuilt = models.CharField(max_length=4, verbose_name="Рік будівництва",
            null=True, blank=True)
    YearRenovation = models.CharField(max_length=4,
            verbose_name="Рік останньої реновації",  null=True, blank=True)
    Architecture = models.CharField(max_length=20, verbose_name="Архітектурний стиль",
            choices=(
                ('empire', 'ампір'),
                ('classicism', 'класицизм'),
                ('chalet', 'шале'),
                ('constructivism', 'конструктивізм'),
                ('hi-tech', 'хай-тек'),
                ('renaissance', 'ренесанс'),
                ('baroque', 'барокко'),
                ('modern', 'модерн'),
                ('other', 'інший'),),
            default='classicism')
    # MSZoning: Identifies the general zoning classification of the sale.
    MSZoning = models.CharField(verbose_name='Зонування', max_length=3,
            choices=(
                ('A',	'СІЛЬСЬКЕ ГОСПОДАРСТВО'),
                ('C',	'КОМЕРЦІЙНА'),
                ('FV',	'ПРИМІСЬКА'),
                ('I',	'ПРОМИСЛОВА'),
                ('RH',	'ВИСОКА ЩІЛЬНІСТЬ ЗАБУДОВИ'),
                ('RL',	'НИЗЬКА ЩІЛЬНІСТЬ ЗАБУДОВИ'),
                ('RP',	'КОТЕДЖНЕ МІСТЕЧКО З НИЗЬКОЮ ЩІЛЬНІСТЮ ЗАБУДОВИ'),
                ('RM',	'СЕРЕДНЯ ЩІЛЬНІСТЬ ЗАБУДОВИ')),
            default='A',
            help_text="Визначає загальну класифікацію зонування продажу")

    # Walls
    Walls = models.CharField(max_length=20, verbose_name="Основний матеріал стін",
            choices=(
                ('SilBrick', 'Силікатна цегла'),
                ('RedBrick', 'Червона цегла'),
                ('CerBlock', 'Керамоблок'),
                ('Wood', "Дерев'яний'"),
                ('CindBlock', 'Шлакоблочний'),
                ('AirConcrete', 'Газоблок'),
                ('SIP', 'СІП панель'),
                ('Other', 'Інше'),),
            default="Other")
    # RoofMatl: Roof material
    RoofMatl = models.CharField(max_length=20, verbose_name="Матеріал даху",
            choices=(
                ('MetalTile', 'металочерепиця'),
                ('Metal', 'Метал'),
                ('ClyTile', 'керамічна черепиця'),
                ('BitumTile', 'Бітумна черепиця'),
                ('CemTile', 'Пісчано-цементна черепиця'),
                ('Shale', 'Сланцеве покриття'),
                ('Slate', 'Шифер'),
                ('Other', 'Інше'),
            ),
            default='Other')
    Foundation = models.CharField(max_length=255, verbose_name="Матеріал, тип, глибина, стан фундаменту",
                null=True, blank=True)
    FirstFloor = models.CharField(max_length=20, verbose_name="Загальна площа 1 поверху, кв.м",
                null=True, blank=True)
    SecondFloor = models.CharField(max_length=20, verbose_name="Площа 2-го поверху",
                null=True, blank=True)
    LowQualFinSF = models.CharField(max_length=20, verbose_name="Площа де ремонт незакінчено або обробка інтер'єру низької якості, усі поверхи, кв.м",
                null=True, blank=True)
    GrLivArea = models.CharField(max_length=20, verbose_name="Уся житлова площа над рівнем землі, кв.м",
                null=True, blank=True)
    Bedroom = models.CharField(max_length=2, verbose_name="Кількість спалень над рівнем землі",
                null=True, blank=True)
    TotRmsAbvGrd = models.CharField(max_length=2, verbose_name="Кількість кімнат над рівнем землі",
                null=True, blank=True)
    Kitchen = models.CharField(max_length=2, verbose_name="Загальний стан кухні",
            choices=(
                ('Ex', 'Преміум'),
                ('Gd', 'Добрий'),
                ('TA', 'Середній'),
                ('Fa', 'Мінімально достатній'),
                ('Po', 'Бідний')),
            default='TA')
    Bathroom = models.CharField(max_length=20, verbose_name="Санвузол",
            choices=(
                ('different', 'Роздільний'),
                ('adjacent', 'Суміжний'),
                ('two_and_more', '2 і більше'),
                ('no_bathrooms', 'Санвузол відсутній'),
            ),
            default='different')
    Repair = models.CharField(max_length=20, verbose_name="Ремонт інтер'єру",
            choices=(
                ('authors_project', 'Авторський проект'),
                ('european_repair', 'Євроремонт'),
                ('cosmetical_repair', 'Косметичний ремонт'),
                ('life_condition', 'Житловий стан'),
                ('after_construction', 'Після будівельників'),
                ('for_clean_processing', 'під чистову обробку'),
                ('emergency_condition', 'Аварійний стан'),),
            default='life_condition')
    Heating = models.CharField(max_length=25, verbose_name="Опалення",
            choices=(
                ('centralize', 'Централізоване'),
                ('own_boiler_room', 'Власна котельня'),
                ('individual_gas', 'Індивідуальне газове'),
                ('individual_electricity', 'Індивідуальне електричне'),
                ('hard_fuel', 'Твердопаливне'),
                ('heat_pump', 'Тепловий насос'),
                ('combination', 'Комбіноване'),
                ('other', 'Інше'),),
            default='other')
    # LAND CONTOUR
    # LotFrontage: Linear feet of street connected to property
    LotFrontage = models.PositiveIntegerField(verbose_name="Лицьова сторона власності, метрів",
                help_text="Довжина вулиці в метрах, де приєднана власність", null=True, blank=True)
    # LotShape: General shape of property
    LotShape = models.CharField(max_length=3, verbose_name="Форма земельної ділянки",
            choices=(
                ('Reg', 'Правильна форма'),
                ('IR1', 'Майже правильна'),
                ('IR2', 'Помірно неправильна'),
                ('IR3', 'Дуже неправильна')),
            default='Reg')
    # LandContour: Flatness of the property
    LandContour = models.CharField(max_length=3, verbose_name="Плоскість власності",
                choices=(
                    ('Lvl', 'Все в одному рівні, плоска ділянка'),
                    ('Bnk', 'Швидкий і значний підйом з вулиці в будівлю'),
                    ('HLS', 'Значний нахил ділянки з боку в бік'),
                    ('Low', 'Нижче рівня вулиці, улоговина'),
                    ('Slp', 'Помірний рівномірний схил')),
                default='Lvl')
    # EXTERIOR
    Exterior = models.CharField(max_length=160, verbose_name="Матеріали фінішної обробки фасаду",
            null=True, blank=True)
    ExterCond = models.CharField(max_length=2, verbose_name="Загальний стан екстер'єру будинку",
            choices=(
                ('Ex', 'Преміум'),
                ('Gd', 'Добрий'),
                ('TA', 'Середній'),
                ('Fa', 'Мінімально достатній'),
                ('Po', 'Бідний')),
                default='TA')
    # GARAGE
    # GarageType: Garage location
    GarageType = models.CharField(max_length=20, verbose_name="Тип гаражу",
                choices=(
                    ('2Types', 'Більше чим 1 тип гаражу'),
                    ('Attchd', 'Гараж приєднаний до будинку'),
                    ('Basment', 'Гараж у фундаменті, підземний'),
                    ('BuiltIn', 'Гараж - частина будинку, має кімнату зверху'),
                    ('CarPort', 'Навіс для машини'),
                    ('Detchd', 'Гараж окремо від будинку'),
                    ('NA', 'Немає гаражу'),),
                default='NA')
    GarageYrBlt = models.CharField(max_length=4, verbose_name='Рік побудови гаражу',
            null=True, blank=True)
    GarageFinish = models.CharField(max_length=3, verbose_name="Інтер'єр, обробка",
                choices=(
                    ('Fin', 'Закінчена, чистова'),
                    ('Rfn', 'Чорнова, часткова'),
                    ('Unf', 'Незакінчена'),
                    ('NA', 'Немає гаражу')),
                default='NA')
    GarageCars = models.CharField(max_length=1, verbose_name='Розмір гаражу, кількість машин',
                null=True, blank=True)
    GarageArea = models.CharField(max_length=7, verbose_name='Площа гаражу, кв.м',
                null=True, blank=True)
    GarageCond = models.CharField(max_length=2, verbose_name='Загальний стан гаражу',
                choices=(
                    ('Ex', 'Преміум'),
                    ('Gd', 'Добре'),
                    ('TA', 'Типова/середня'),
                    ('Fa', 'Достатньо чисто'),
                    ('Po', 'Бідно'),
                    ('NA', 'Немає гаражу')),
                default='NA')
    # POOL
    PoolArea = models.CharField(max_length=7, verbose_name='Загальна площа басейну, кв.м',
                null=True, blank=True)
    PoolQC = models.CharField(max_length=2, verbose_name='Загальний стан басейну',
                choices=(
                    ('Ex', 'Преміум'),
                    ('Gd', 'Добре'),
                    ('TA', 'Типова/середня'),
                    ('Fa', 'Достатньо чисто'),
                    ('Po', 'Бідно'),
                    ('NA', 'Немає басейну')),
                default='NA')
    # FENCE
    Fence = models.CharField(max_length=6, verbose_name="Якість паркану, огорожі",
            choices=(
                ('GdPrv', 'Добре захищена приватність'),
                ('MnPrv', 'Мінімальна приватність'),
                ('BadPrv', 'Погано захищена приватність'),
                ('NA', 'Немає огорожі')),
            default='NA')
    # FIREPLACE
    Fireplace = models.CharField(max_length=160, verbose_name="Камін, тип, якість, стан",
                null=True, blank=True)
    # BODY TEXT
    body = models.TextField(max_length=4000, verbose_name='Опис',
            help_text="<em>до 4000 знаків</em>")
    # Appliances
    plate = models.BooleanField(verbose_name='Плита')
    cooking_plate = models.BooleanField(verbose_name='Варочна поверхня')
    oven = models.BooleanField(verbose_name='Духова шафа')
    microwave = models.BooleanField(verbose_name='Мікрохвильова піч')
    refrigerator = models.BooleanField(verbose_name='Холодильник')
    dishwashers = models.BooleanField(verbose_name='Посудомийна машина')
    washing_machine = models.BooleanField(verbose_name='Пральна машина')
    dryer = models.BooleanField(verbose_name='Сушильна машина')

    # Multimedia
    wi_fi = models.BooleanField(verbose_name='WI-FI')
    high_speed_internet = models.BooleanField(
                        verbose_name='Швидкісний інтернет')
    tv = models.BooleanField(verbose_name='Телевізор')
    cable_digital_tv = models.BooleanField(verbose_name='Кабельнеб цифрове ТБ')
    satellite_tv = models.BooleanField(verbose_name='Супутникове ТБ')

    # Comfort
    air_conditioning = models.BooleanField(verbose_name='Кондиціонер')
    floor_heating = models.BooleanField(verbose_name='Підігрів підлоги')
    cleaner = models.BooleanField(verbose_name='Центральний пилосос')
    bath = models.BooleanField(verbose_name='Ванна')
    shower  = models.BooleanField(verbose_name='Душ')
    kitchen_furniture = models.BooleanField(verbose_name='Меблі на кухні')
    wardrobe = models.BooleanField(verbose_name='Гардероб')
    balcony = models.BooleanField(verbose_name='Балкон')
    terrace = models.BooleanField(verbose_name='Тераса')
    panoramic_windows = models.BooleanField(verbose_name='Панорамні вікна')
    grid_on_the_windows = models.BooleanField(verbose_name='Грати на вікнах')
    alarms = models.BooleanField(verbose_name='Сигналізація')
    fire_alarm = models.BooleanField(verbose_name='Пожежна сигналізація')
    video_surveillance = models.BooleanField(verbose_name='Відеоспостереження')
    protection_of_the_territory = models.BooleanField(
                                verbose_name='Охорона території')
    elevator = models.BooleanField(verbose_name='Ліфт')
    tennis_court = models.BooleanField(verbose_name="Тенісний корт", default=False)
    bbarbecue = models.BooleanField(verbose_name="Бесідка, мангал, барбекю", default=False)
    pantry = models.BooleanField(verbose_name='Сарай більше 50 кв.м')
    smart_home_technology = models.BooleanField(
                          verbose_name='Технологія "розумний будинок"')
    autonomous_generator = models.BooleanField(
                         verbose_name='Автономний електрогенератор')
    # Communications
    gas = models.BooleanField(verbose_name='Газ')
    central_water_supply = models.BooleanField(
                         verbose_name='Центральний водопровід')
    well = models.BooleanField(verbose_name='Скважина')
    electricity = models.BooleanField(verbose_name='Електрика')
    central_sewerage = models.BooleanField(
                     verbose_name='Центральна каналізація')
    septic_tank = models.BooleanField(verbose_name='Каналізація септик')
    removal_of_waste = models.BooleanField(verbose_name='Вивіз відходів')
    asphalt_road = models.BooleanField(verbose_name='Асфальтована дорога')

    # Infrastructure (up to 500 meters)
    kindergarten = models.BooleanField(verbose_name='Дитячий садок')
    school = models.BooleanField(verbose_name='Школа')
    the_pump_room = models.BooleanField(verbose_name='Бювет')
    transportation_stop = models.BooleanField(verbose_name='Зупинка транспорту')
    market = models.BooleanField(verbose_name='Ринок')
    shop_kiosk = models.BooleanField(verbose_name='Магазин, кіоск')
    supermarket_mall = models.BooleanField(verbose_name='Супермаркет, ТРЦ')
    park_green_area = models.BooleanField(verbose_name='Парк, зелена зона')
    playground = models.BooleanField(verbose_name='Дитячий майданчик')
    pharmacy = models.BooleanField(verbose_name='Аптека')
    hospital_clinic = models.BooleanField(verbose_name='Лікарня, поліклініка')
    city_center = models.BooleanField(verbose_name='Центр міста')
    restaurant_cafe = models.BooleanField(verbose_name='Ресторан, кафе')
    cinema_theater = models.BooleanField(verbose_name='Кінотеатр, театр')
    post_office = models.BooleanField(verbose_name='Відділення пошти')
    bank_branch_ATM = models.BooleanField(
                    verbose_name='Відділення банку, банкомат')
    bus_station = models.BooleanField(verbose_name='Автовокзал')
    railway_station = models.BooleanField(verbose_name='Залізнична станція')

    # Landscape (up to 1 km.)
    river = models.BooleanField(verbose_name='Річка')
    reservoir = models.BooleanField(verbose_name='Водосховище')
    lake = models.BooleanField(verbose_name='Озеро')
    hills = models.BooleanField(verbose_name='Пагорби')
    mountains = models.BooleanField(verbose_name='Гори')
    park = models.BooleanField(verbose_name='Парк')
    forest = models.BooleanField(verbose_name='Ліс')

    # ADDRESS
    address = models.CharField(max_length=255, verbose_name='Адреса', null=True, blank=True)
    # INVISIBLE FIELDS IN FORM
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
               related_name='houses', verbose_name='Власник оголошення',
               null=True,)
    slug = models.SlugField(default='', editable=False, max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    num_visits = models.PositiveIntegerField(default=0)

    # PREPROCESSING ADDRESS
    def _generate_address(self):
        location = geolocator.reverse((self.geometry.y, self.geometry.x))
        addr = location.address
        addr_split = addr.split(',')
        address = ', '.join(addr_split[:-4])
        self.address = address

    @property
    def popupCoords(self):
        lat = round(self.geometry.y, 6)
        lng = round(self.geometry.x, 6)
        return f'{lat}, {lng}'

    # META CLASS
    class Meta:
        ordering = ["-pub_date",]

    # TO STRING METHOD
    def __str__(self):
        return self.title

    # PREPROCESSING SLUGS
    def _generate_slug(self):
        value = translit(self.title[:70])
        slug_candidate = slugify(value, allow_unicode=True)
        # ctime = datetime.datetime.now().ctime()
        self.slug = f'{slug_candidate}'

    # SAVE METHOD
    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
            self._generate_address()
        super().save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        """ Returns the url to access a detail record for this offer."""
        return reverse('house', kwargs={'pk': self.pk, 'slug': self.slug})
