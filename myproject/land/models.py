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
	title = models.CharField(max_length=70, verbose_name='Заголовок оголошення', help_text='до 70 знаків')
	geometry = geomodels.PolygonField(verbose_name='Площа на мапі',  extent=(31.44, 49.217, 32.47, 49.68), 
			 help_text='<em>обведіть багатокутник по формі земельної ділянки</em>')
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
    # Landscape (up to 1 km.)
    river = models.BooleanField(verbose_name='Річка')
    reservoir = models.BooleanField(verbose_name='Водосховище')
    lake = models.BooleanField(verbose_name='Озеро')
    hills = models.BooleanField(verbose_name='Пагорби')
    mountains = models.BooleanField(verbose_name='Гори')
    park = models.BooleanField(verbose_name='Парк')
    forest = models.BooleanField(verbose_name='Ліс')

    # INVISIBLE FIELDS IN FORM
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
               related_name='lands', verbose_name='Власник оголошення',
               null=True,)
    slug = models.SlugField(default='', editable=False, max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    num_visits = models.PositiveIntegerField(default=0)

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
            # self._generate_address()
        super().save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        """ Returns the url to access a detail record for this offer."""
        return reverse('land', kwargs={'slug': self.slug})    