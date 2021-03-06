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
    geometry = geomodels.PointField(verbose_name='Місце на мапі',
             extent=(31.00, 49.00, 33.00, 50.00),
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
    price = models.PositiveIntegerField(verbose_name='Ціна, $')
    currency = models.CharField(verbose_name='Валюта', max_length=3,
             choices=(('UAH', 'грн.'), ('USD', 'USD'),),
             blank=False, default='USD',)

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
                    ('20',  '1-поверховий після 2000р., всі стилі'),
                    ('30',  '1-поверховий до 1999р.'),
                    ('40',	'1-поверх + мансарда, Незакінчений всі роки'),
                    ('50',	'1-поверх + мансарда, Закінчений всі роки'),
                    ('60',	'2-поверховий після 2000р.'),
                    ('70',	'2-поверховий до 1999р.'),
                    ('75',	'2-поверховий + мансарда всі роки'),
                    ('80',	'Багаторівневий'),
                    ('90',	'Кількаповерховий з фойе'),
                    ('110',	'Дуплекс, Таунхаус - усі стилі після 2010р.'),
                    ('120',	'1-поврховий типовий радянський проект після 1960р.'),
                    ('150',	"на 2 сім'ї - типовий радянський проект")),
                verbose_name="Тип об'єкта",
                default='20')
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
    GrLivArea = models.CharField(max_length=20, verbose_name="Уся житлова площа, кв.м",
                null=True, blank=True)
    Bedroom = models.CharField(max_length=2, verbose_name="Кількість спалень",
                null=True, blank=True)
    TotRmsAbvGrd = models.CharField(max_length=2, verbose_name="Кількість кімнат",
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
    # GARAGE
    # GarageType: Garage location
    GarageType = models.CharField(max_length=20, verbose_name="Гараж",
                choices=(
                    ('2Types', 'Більше чим 1 тип гаражу'),
                    ('Attchd', 'Гараж приєднаний до будинку'),
                    ('Basment', 'Гараж у фундаменті, підземний'),
                    ('BuiltIn', 'Гараж - частина будинку, має кімнату зверху'),
                    ('CarPort', 'Навіс для машини'),
                    ('Detchd', 'Гараж окремо від будинку'),
                    ('NA', 'Немає гаражу'),),
                default='NA')
    # FENCE
    Fence = models.CharField(max_length=6, verbose_name="Паркан, огорожа",
            choices=(
                ('GdPrv', 'Добре захищена приватність'),
                ('MnPrv', 'Мінімальна приватність'),
                ('BadPrv', 'Погано захищена приватність'),
                ('NA', 'Немає огорожі')),
            default='GdPrv')
    # LAND CONTOUR
    # LandArea: Total square meter of land
    LandArea = models.DecimalField(verbose_name='Загальна площа земельної ділянки, га',
             max_digits=10, decimal_places=2, null=True, blank=True)
    CadastrNumber = models.CharField(verbose_name='Кадастровий номер',
            max_length=30, blank=True, null=True)
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
    cable_digital_tv = models.BooleanField(verbose_name='Кабельне або супутникове ТБ')

    # ADDRESS
    address = models.CharField(max_length=255, verbose_name='Адреса', null=True,
            blank=True)
    # INVISIBLE FIELDS IN FORM
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
               related_name='houses', verbose_name='Власник оголошення',
               null=True,)
    slug = models.SlugField(default='', editable=False, max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    num_visits = models.PositiveIntegerField(default=0)
    # new field for archivate offers
    archive = models.BooleanField(verbose_name="Оголошення в архіві",
            default=False)
    archivated_date = models.DateTimeField(null=True, blank=True)
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
        ctime = datetime.datetime.now().ctime()
        self.slug = f'{slug_candidate}-{ctime}'

    # SAVE METHOD
    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
            self._generate_address()
        # delete old file when replacing by updating the file
        try:
            this = House.objects.get(id=self.id)
            if this.image1 != self.image1:
                this.image.delete(save=False)
            if this.image2 != self.image2:
                this.image.delete(save=False)
            if this.image3 != self.image3:
                this.image.delete(save=False)
            if this.image4 != self.image4:
                this.image.delete(save=False)
            if this.image5 != self.image5:
                this.image.delete(save=False)
            if this.image6 != self.image6:
                this.image6.delete(save=False)
            if this.image7 != self.image7:
                this.image7.delete(save=False)
            if this.image8 != self.image8:
                this.image8.delete(save=False)
            if this.image9 != self.image9:
                this.image9.delete(save=False)
        except: pass # when new images then we do nothing, normal case
        super().save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        """ Returns the url to access a detail record for this offer."""
        return reverse('house', kwargs={'pk': self.pk, 'slug': self.slug})

##========================================================================
## SIGNALS

def delete_image(sender, instance, **kwargs):
    if instance.image1:
        instance.image1.delete(False)
    if instance.image2:
        instance.image2.delete(False)
    if instance.image3:
        instance.image3.delete(False)
    if instance.image4:
        instance.image4.delete(False)
    if instance.image5:
        instance.image5.delete(False)
    if instance.image6:
        instance.image6.delete(False)
    if instance.image7:
        instance.image7.delete(False)
    if instance.image8:
        instance.image8.delete(False)
    if instance.image9:
        instance.image9.delete(False)

models.signals.pre_delete.connect(delete_image, sender=House)
