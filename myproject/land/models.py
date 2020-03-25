import datetime
from translitua import translit
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim

geolocator = Nominatim(timeout=7, user_agent='land')

class Land(models.Model):
    # GENERAL FIELDS
    type_offer = models.CharField(max_length=50, verbose_name="Тип оголошення",
                choices=(
                    ('sale', 'Продаж'),
                    ('rent', 'Оренда довгострокова')),
                default='SALE')
    title = models.CharField(max_length=70, verbose_name='Заголовок оголошення',
          help_text='до 70 знаків')
    geometry = geomodels.PolygonField(verbose_name='Площа на мапі',
             extent=(31.00, 49.00, 33.00, 50.00),
			 help_text='<em>багатокутник по формі земельної ділянки</em>')
    price = models.PositiveIntegerField(verbose_name='Ціна')
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
    # cadastral number
    cadastral_number = models.CharField(max_length=25, verbose_name="Кадастровий номер",
                     null=True, blank=True)
    # MSZoning: Identifies the general zoning classification of the sale.
#     ID	Тип ділянки	Коротка назва
# 1	Для будівництва й обслуговування житлового будинку, господарських будівель і споруд (присадибна ділянка)	ОЖБ
# 2	Для ведення особистого селянського господарства й подібні	ОСГ
# 3	Для індивідуального й колективного садівництва та дачного будівництва	Cадова
# 4	Під комерційну діяльність та інші, що не ввійшли до решти груп	Комерційна
# 5	Під багатоквартирний будинок	Багатоповерхова
# 6	Для ведення товарного сільського господарства й подібні	Товарна
# 7	Одна з ділянок під ОЖБ, а одна під ОСГ	ОЖБ й ОСГ
    MSZoning = models.CharField(verbose_name='Тип земельної ділянки', max_length=3,
            choices=(
                ('A',	'Присадибна ділянка для будівництва приватного будинку'),
                ('C',	'Особисте селянське господарство'),
                ('FV',	'Садова або дачне будівництво'),
                ('I',	'Комерційна діяльність'),
                ('RH',	'Під багатоквартирний будинок'),
                ('RL',	'НИЗЬКА ЩІЛЬНІСТЬ ЗАБУДОВИ'),
                ('RP',	'Для ведення товарного сільського господарства'),
                ('RM',	'Приватний будинок + особисте селянське господарство')),
            default='A',)
    # LAND CONTOUR
    # LandArea: Total square meter of land
    LandArea = models.DecimalField(verbose_name='Загальна площа земельної ділянки, га',
             max_digits=10, decimal_places=2, null=True, blank=True)
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
    # FENCE
    Fence = models.CharField(max_length=6, verbose_name="Якість паркану, огорожі",
            choices=(
                ('GdPrv', 'Добре захищена приватність'),
                ('MnPrv', 'Мінімальна приватність'),
                ('BadPrv', 'Погано захищена приватність'),
                ('NA', 'Немає огорожі')),
            default='NA')

    # BODY TEXT
    body = models.TextField(max_length=4000, verbose_name='Опис',
            help_text="<em>до 4000 знаків</em>")

    # INVISIBLE FIELDS IN FORM
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
               related_name='lands', verbose_name='Власник оголошення',
               null=True,)
    slug = models.SlugField(default='', editable=False, max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    num_visits = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=255, verbose_name='Адреса',
            blank=True, null=True)
    # new field for archivate offers
    archive = models.BooleanField(verbose_name="Оголошення в архіві",
            default=False)
    archivated_date = models.DateTimeField(null=True, blank=True)
    # PREPROCESSING ADDRESS
    def _generate_address(self):
        location = geolocator.reverse(self.lat_lng)
        addr = location.address
        # addr_split = addr.split(',')
        # address = ', '.join(addr_split[:-4])
        # self.address = address
        self.address = addr
    # META CLASS
    class Meta:
        ordering = ["-pub_date",]

    # TO STRING METHOD
    def __str__(self):
        return self.title

    # POLYGON AND CENTER COORDINATES TO MAP
    @property
    def polygon(self):
        coords = self.geometry.coords[0]
        polygon = [list(item)[::-1] for item in coords]
        return polygon
    @property
    def lat_lng(self):
        lat = round(getattr(self.geometry, 'coords')[0][0][1], 6)
        lng = round(getattr(self.geometry, 'coords')[0][0][0], 6)
        return [lat, lng]

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
            this = Land.objects.get(id=self.id)
            if this.image1 != self.image1:
                this.image.delete(save=False)
        except: pass # when new images then we do nothing, normal case
        super().save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        """ Returns the url to access a detail record for this offer."""
        return reverse('land', kwargs={'slug': self.slug})


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

models.signals.pre_delete.connect(delete_image, sender=Land)
