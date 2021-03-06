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
    ('authors_project', 'Авторський проект'),
    ('european_repair', 'Євроремонт'),
    ('cosmetical_repair', 'Косметичний ремонт'),
    ('life_condition', 'Житловий стан'),
    ('after_construction', 'Після будівельників'),
    ('for_clean_processing', 'під чистову обробку'),
    ('emergency_condition', 'Аварійний стан'),
)
class Offer(models.Model):
    """ Define a row of flat in database.
    """
    # GEOMETRY FIELD
    geometry = geomodels.PointField(verbose_name='Місце на мапі',
             extent=(31.00, 49.00, 33.00, 50.00),
             help_text='<em>Просто поставте маркер на карту</em>')
    # create latitude and longitude coordinates for leaflet map:
    @property
    def lat_lng(self):
        return list(getattr(self.geometry, 'coords', [])[::-1])
    # GENERAL FIELDS
    type_offer = models.CharField(max_length=5, verbose_name="Тип оголошення",
               choices=TYPE_OFFER,default='sale')
    title = models.CharField(max_length=70, verbose_name='Заголовок',
          help_text='до 70 знаків, повторно не редагується!', blank=False)
    type_object = models.CharField(max_length=10, choices=TYPES_OBJECT,
                    verbose_name="Тип об'єкта", default='flat')
    price = models.PositiveIntegerField(verbose_name='Ціна')
    currency = models.CharField(verbose_name='Валюта', max_length=3,
             choices=(('UAH', 'грн.'),('USD', 'USD'),), blank=False, default='USD',)
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
    walls = models.CharField(max_length=15, verbose_name='Матеріал стін',
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
    # BODY TEXT
    body = models.TextField(max_length=2000, verbose_name='Опис',
            help_text="<em>до 2000 знаків</em>")
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
    cable_digital_tv = models.BooleanField(verbose_name='Кабельнеб або супутникове ТБ')

    # ADDRESS
    address = models.CharField(max_length=255, verbose_name='Адреса', null=True, blank=True)
    # INVISIBLE FIELDS IN FORM
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
               related_name='flats', verbose_name='Власник оголошення',
               null=True,)
    slug = models.SlugField(default='', editable=False, max_length=100)
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
        value = translit(self.title)
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
            this = Offer.objects.get(id=self.id)
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
        return reverse('offer-detail',
                        kwargs={'pk': self.pk, 'slug': self.slug})


##=========================================================================
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

models.signals.pre_delete.connect(delete_image, sender=Offer)
