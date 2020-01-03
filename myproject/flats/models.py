import datetime
from translitua import translit
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

from geopy.geocoders import Nominatim

geolocator = Nominatim(timeout=7, user_agent='flats')

# CHOICES
TYPE_OFFER = (
    ('sale', 'Продаж'),
    ('rent', 'Оренда довгострокова'),
)
YESNO = (('yes','Так'),('no', 'Ні'))
TYPES_OBJECT = (
    ('flat', 'Квартира'),
    ('part_flat', 'Частина квартири'),
    ('room', 'Кімната')
)
CURRENCY = (('UAH', 'грн.'), ('USD', 'USD'))
BUILDING_TYPE = (
    ('royal', 'Царський будинок'),
    ('stalin', 'Сталінка'),
    ('hruschov', 'Хрущовка'),
    ('czech',  'Чешка'),
    ('guest',  'Гостинка'),
    ('sovmin', 'Совмін'),
    ('hostel', 'Гуртожиток'),
    ('90',   'Житловий фонд 80-90'),
    ('2000', 'Житловий фонд 91-2000'),
    ('2010', 'Житловий фонд 2001-2010'),
    ('2019', 'Житловий фонд від 2011'),
    ('constraction', 'На етапі будівництва')
)
WALLS = (
    ('brick', 'Цегляний'),
    ('panel', 'Панельний'),
    ('monolit', 'Монолітний'),
    ('wood', "Дерев'яний'"),
    ('cinder_block', 'Шлакоблочний'),
    ('air_concrete', 'Газоблок'),
    ('sip', 'СІП панель'),
    ('other', 'Інше'),
)
PLANNING = (
    ('adjacent', 'Суміжна, прохідна'),
    ('different', 'Роздільна'),
    ('studio', 'Студія'),
    ('penthouse', 'Пентхаус'),
    ('multilevel', 'Багаторівнева'),
    ('small_family', 'Малосімейка, гостинка'),
    ('smart_flat', 'Смарт-квартира'),
    ('free_planning', 'Вільне планування'),
    ('two_sides', 'Двостороння'),
)
BATHROOM = (
    ('different', 'Роздільний'),
    ('adjacent', 'Суміжний'),
    ('two_and_more', '2 і більше'),
    ('no_bathrooms', 'Санвузол відсутній'),
)
HEATING = (
    ('centralize', 'Централізоване'),
    ('own_boiler_room', 'Власна котельня'),
    ('individual_gas', 'Індивідуальне газове'),
    ('individual_electricity', 'Індивідуальне електричне'),
    ('hard_fuel', 'Твердопаливне'),
    ('heat_pump', 'Тепловий насос'),
    ('combination', 'Комбіноване'),
    ('other', 'Інше'),
)
REPAIR = (
    ('None', 'Виберіть стан ремонту'),
    ('authors_project', 'Авторський проект'),
    ('european_repair', 'Євроремонт'),
    ('cosmetical_repair', 'Косметичний ремонт'),
    ('life_condition', 'Житловий стан'),
    ('after_construction', 'Після будівельників'),
    ('for_clean_processing', 'під чистову обробку'),
    ('emergency_condition', 'Аварійний стан'),
)
DISTRICTS = (
    ('Райони', (
    ('700-richchia', '700-річчя'),
    ('Vantazhnyi port', 'Вантажний порт'),
    ('Vodokanal-Nevskoho', 'Водоканал-Невського'),
    ('Dakhnivka', 'Дахнівка'),
    ('Dniprovskyi', 'Дніпровський'),
    ('Zaliznychnyi vokzal', 'Залізничний вокзал'),
    ('Zelena', 'Зелена'),
    ('k-t Myr', 'к-т Мир'),
    ('Kazbet', 'Казбет'),
    ('Litak', 'Літак'),
    ('Lunacharskyi', 'Луначарський'),
    ('Mytnytsia', 'Митниця'),
    ('Mytnytsia-richport', 'Митниця-річпорт'),
    ('Mytnytsia-tsentr', 'Митниця-центр'),
    ('PZR', 'ПЗР'),
    ('Prydniprovskyi', 'Придніпровський'),
    ('Piatykhatky', 'Пятихатки'),
    ('Raion D', 'Район Д'),
    ('Siedova', 'Сєдова'),
    ('Sosnivka', 'Соснівка'),
    ('Sosnivskyi', 'Соснівський'),
    ('Khimselyshche', 'Хімселище'),
    ('Tsentr', 'Центр'),
    ('Shkilna', 'Шкільна'),
    ('Yabluchnyi', 'Яблучний'))
    ),
    ('Передмістя', (
    ('Biloziria', "Білозір'я"),
    ('Heronymivka', 'Геронимівка'),
    ('Orshanets', 'Оршанець'),
    ('Ruska Poliana', 'Руська Поляна'),
    ('Chervona Sloboda', 'Червона Слобода'))
    ),
    ('Села', (
    ('Yelyzavetovka', 'Єлизаветовка'),
    ('Irdyn', 'Ірдинь'),
    ('Baibuzy', 'Байбузи'),
    ('Berezniaky', 'Березняки'),
    ('Budyshche', 'Будище'),
    ('Buzukiv', 'Бузуків'),
    ('Verhuny', 'Вергуни'),
    ('Dubiivka', 'Дубіївка'),
    ('Dumantsi', 'Думанці'),
    ('Kumeiky', 'Кумейки'),
    ('Lesky', 'Леськи'),
    ('Lozivok', 'Лозівок'),
    ('Moshny', 'Мошни'),
    ('Moshnohiria', "Мошногір'я"),
    ('Nechaivka', 'Нечаївка'),
    ('Novoselivka', 'Новоселівка'),
    ('Pervomaiske', 'Первомайське'),
    ('Sahunivka', 'Сагунівка'),
    ('Svitanok', 'Світанок'),
    ('Svydivok', 'Свидівок'),
    ('Sokyrno', 'Сокирно'),
    ('Sofiivka', 'Софіївка'),
    ('Stepanky', 'Степанки'),
    ('Tubiltsi', 'Тубільці'),
    ('Khatsky', 'Хацьки'),
    ('Khreshchatyk', 'Хрещатик'),
    ('Khudiaky', 'Худяки'),
    ('Khutory', 'Хутори'),
    ('Chorniavka', 'Чорнявка'),
    ('Shelepukhy', 'Шелепухи'),
    ('Yasnoziria', "Яснозір'я"))
    ),
)
class Offer(models.Model):
    """ Define a row of flat in database.
    """
    # GEOMETRY FIELD
    geometry = geomodels.PointField(extent=(31.44, 49.217, 32.47, 49.68))
    # create latitude and longitude coordinates for leaflet map:
    @property
    def lat_lng(self):
        return list(getattr(self.geometry, 'coords', [])[::-1])
    # GENERAL FIELDS
    type_offer = models.CharField(max_length=5, verbose_name="Тип оголошення",
               choices=TYPE_OFFER,default='sale')
    title = models.CharField(max_length=70, verbose_name='Заголовок',
          help_text='70 знаків', blank=False)
    type_object = models.CharField(max_length=10, choices=TYPES_OBJECT,
                    verbose_name="Тип об'єкта", default='flat')
    price = models.PositiveIntegerField(verbose_name='Ціна')
    currency = models.CharField(verbose_name='Валюта', max_length=3,
             choices=CURRENCY, blank=False, default='USD',)

    # COLLABORATION
    agree_price = models.BooleanField('Договірна')
    no_commission = models.BooleanField(verbose_name='Без комісії')
    exchange = models.BooleanField(verbose_name='Можливість обміну')
    collaboration = models.BooleanField(
        verbose_name='Готовий співпрацювати з ріелторами')

    # CONSTRACTION PARAMETERS
    building = models.CharField(max_length=12,choices=BUILDING_TYPE,
             verbose_name='Тип будинку', )
    floor = models.PositiveSmallIntegerField(verbose_name='Поверх')
    total_floor = models.PositiveSmallIntegerField(verbose_name='Поверхів')
    area = models.PositiveSmallIntegerField(verbose_name='Загальна площа, кв.м')
    kitchen = models.PositiveSmallIntegerField(verbose_name='Кухня площа, кв.м')
    walls = models.CharField(max_length=10, verbose_name='Матеріал стін',
          choices=WALLS)
    rooms = models.PositiveSmallIntegerField(verbose_name='Кількість кімнат')
    planning = models.CharField(max_length=14, choices=PLANNING,
             verbose_name='Планування квартири', )
    bathroom = models.CharField(max_length=14, verbose_name='Санвузол',
             choices=BATHROOM)
    heating = models.CharField(max_length=24, verbose_name='Опалення',
            choices=HEATING)
    repair = models.CharField(max_length=24, verbose_name='Ремонт',
           choices=REPAIR)
    furniture = models.CharField(max_length=3, verbose_name='Меблювання',
              choices=( ('yes', 'Так'), ('no', 'Ні')),)
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
    bath = models.BooleanField(verbose_name='Ванна')
    shower  = models.BooleanField(verbose_name='Душ')
    kitchen_furniture = models.BooleanField(verbose_name='Меблі на кухні')
    wardrobe = models.BooleanField(verbose_name='Гардероб')
    balcony = models.BooleanField(verbose_name='Балкон, лоджія')
    terrace = models.BooleanField(verbose_name='Тераса')
    panoramic_windows = models.BooleanField(verbose_name='Панорамні вікна')
    grid_on_the_windows = models.BooleanField(verbose_name='Грати на вікнах')
    alarms = models.BooleanField(verbose_name='Сигналізація')
    fire_alarm = models.BooleanField(verbose_name='Пожежна сигналізація')
    video_surveillance = models.BooleanField(verbose_name='Відеоспостереження')
    concierge = models.BooleanField(verbose_name="Конс'ерж")
    protection_of_the_territory = models.BooleanField(
                                verbose_name='Охорона території')
    parking_space = models.BooleanField(verbose_name='Паркувальне місце')
    guest_parking = models.BooleanField(verbose_name='Гостьовий паркінг')
    underground_parking = models.BooleanField(verbose_name='Підземний паркінг')
    garage = models.BooleanField(verbose_name='Гараж')
    elevator = models.BooleanField(verbose_name='Ліфт')
    freight_elevator = models.BooleanField(verbose_name='Грузовий ліфт')
    pantry = models.BooleanField(verbose_name='Госп. приміщення, комора')
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
    # BODY TEXT
    body = models.TextField(max_length=2000, verbose_name='Опис',
            help_text="<em>до 2000 знаків</em>")
    # ADDRESS
    address = models.CharField(max_length=255, verbose_name='Адреса', null=True, blank=True)
    # INVISIBLE FIELDS IN FORM
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
               related_name='flats', verbose_name='Власник оголошення',
               null=True,)
    slug = models.SlugField(default='', editable=False, max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    num_visits = models.PositiveIntegerField(default=0)

    # SAVING MEDIA FILES
    def user_directory_path(instance, filename):
        img_path = 'user_{0}/{1}'.format(instance.created_by.id, filename)
        return img_path

    image1 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Фото 1', null=True, blank=True)
    image2 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Фото 2', null=True, blank=True)
    image3 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Фото 3', null=True, blank=True)
    image4 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Фото 4', null=True, blank=True)
    image5 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Фото 5', null=True, blank=True)
    image6 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Фото 6', null=True, blank=True)
    image7 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Фото 7', null=True, blank=True)
    image8 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Фото 8', null=True, blank=True)
    image9 = models.ImageField(upload_to=user_directory_path,
            verbose_name='Фото 9', null=True, blank=True)
    # CONTRACT AND INSIDE INFORMATION
    def contract_path(instance, filename):
        contr_path = 'user_{0}/{1}'.format(instance.created_by.id, filename)
        return contr_path

    # PREPROCESSING ADDRESS
    def _generate_address(self):
        location = geolocator.reverse((self.geometry.y, self.geometry.x))
        addr = location.address
        addr_split = addr.split(',')
        address = ', '.join(addr_split[:-4])
        self.address = address

    @property
    def popupCoords(self):
        return (self.geometry.y, self.geometry.x)

    # META CLASS
    class Meta:
        ordering = ["-pub_date",]

    # TO STRING METHOD
    def __str__(self):
        return self.title

    # PREPROCESSING SLUGS
    def _generate_slug(self):
        value = translit(self.title)
        slug_candidate = slugify(value, allow_unicode=True)
        ctime = datetime.datetime.now().ctime()
        self.slug = f'{slug_candidate}-{ctime}'

    # SAVE METHOD
    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
            self._generate_address()
        super().save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        """ Returns the url to access a detail record for this offer."""
        return reverse('offer-detail',
                        kwargs={'pk': self.pk, 'slug': self.slug})
