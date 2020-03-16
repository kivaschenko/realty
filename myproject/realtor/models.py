from translitua import translit
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.gis.db import models as geomodels
from geopy.geocoders import Nominatim
from django.contrib.auth.models import User

geolocator = Nominatim(timeout=7, user_agent='agencys')

class Agency(models.Model):
    geometry = geomodels.PointField(verbose_name='Місце на мапі',
             extent=(31.44, 49.217, 32.47, 49.68),
             help_text='<em>Просто поставте маркер на карту</em>')
    name = models.CharField(verbose_name='Назва агенції', max_length=255)
    phone1 = models.CharField(max_length=13, verbose_name="Телефон основний",
        help_text="міжнародний формат, +38067XXXYYZZ",)
    phone2 = models.CharField(max_length=13, verbose_name="Телефон додатковий",
        help_text="міжнародний формат, +38067XXXYYZZ",)
    body = models.TextField(verbose_name='Про агенство',max_length=2000,
         help_text='<em>До 2000 символів</em>')
    # INVISIBLE FIELDS IN FORM
    address = models.CharField(max_length=255, verbose_name='Адреса',
                               null=True, blank=True)
    created_by = models.OneToOneField(User, on_delete=models.CASCADE,
               verbose_name='Власник сторінки')
    slug = models.SlugField(default='', editable=False, max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    num_visits = models.PositiveIntegerField(default=0)

    logo = models.ImageField(upload_to='media',
            verbose_name='Логотип', null=True, blank=True)
    @property
    def lat_lng(self):
        return list(getattr(self.geometry, 'coords', [])[::-1])
    @property
    def popupCoords(self):
        lat = round(self.geometry.y, 6)
        lng = round(self.geometry.x, 6)
        return f'{lat}, {lng}'
    # META CLASS
    class Meta:
        ordering = ["-name",]
    # TO STRING METHOD
    def __str__(self):
        return self.name
    # PREPROCESSING SLUGS
    def _generate_slug(self):
        value = translit(self.name)
        self.slug = slugify(value, allow_unicode=True)
    # PREPROCESSING ADDRESS
    def _generate_address(self):
        location = geolocator.reverse((self.geometry.y, self.geometry.x))
        addr = location.address
        addr_split = addr.split(',')
        address = ', '.join(addr_split[:-4])
        self.address = address
    # SAVE METHOD
    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
            self._generate_address()
        try:
            this = Agency.objects.get(id=self.id)
            if this.logo != self.logo:
                this.logo.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)
    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        """ Returns the url to access a detail record for the agency.
        """
        return reverse('agency', kwargs={"pk":self.pk, 'slug': self.slug})

##=========================================================================
## SIGNALS FOR AGENCY
def delete_logo(sender, instance, **kwargs):
    if instance.logo:
        instance.logo.delete(False)

models.signals.pre_delete.connect(delete_logo, sender=Agency)

##==========================================================================
## REALTOR MODEL

class Realtor(models.Model):
    """ Model represents all information about rieltor
    """
    phone = models.CharField(max_length=13, verbose_name="Телефон основний",
        help_text="міжнародний формат, +38067XXXYYZZ", unique=True, null=True,
        blank=True)
    start_year = models.CharField(max_length=4,
        verbose_name='Рік початку роботи ріелтором', null=True, blank=True)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL,
            related_name='realtors', null=True, blank=True,
            verbose_name="Агенство",)
    bio = models.TextField(max_length=1000, blank=True, null=True,
        verbose_name="Подробиці про ріелтора",
        help_text="<em>все, що вважаєте за потрібне про себе, \
свою фірму до 1000 знаків</em>",)
    # INVISIBLE FIELDS
    created_by = models.OneToOneField(User, on_delete=models.CASCADE,
               verbose_name='Власник профілю',)
    num_visits = models.PositiveIntegerField(default=0)
    # new
    limit_offers = models.PositiveSmallIntegerField(
                 verbose_name='Ліміт оголошень, штук', default=20)
    offers = models.PositiveSmallIntegerField(verbose_name="Об'єктів на продаж",
            default=0)
    in_archive = models.PositiveSmallIntegerField(
               verbose_name="Об'єктів в архіві", default=0)
    # rating = models.DecimalField(verbose_name='Рейтинг', max_digits=3,
    #     decimal_places=2, default=0.00)

    # SAVING MEDIA FILES
    def user_directory_path(instance, filename):
        img_path = 'user_{0}/{1}'.format(instance.created_by.id, filename)
        return img_path
    avatar = models.ImageField(upload_to=user_directory_path, null=True,
            blank=True, verbose_name='Фото ріелтора')
    # META CLASS
    class Meta:
        ordering = ['pk']
    # TO STRING METHOD
    def __str__(self):
        return f'{self.created_by.first_name} {self.created_by.last_name} - \
                 {self.agency}'
    # SAVE METHOD
    def save(self, *args, **kwargs):
        try:
            this = Realtor.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)
    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        """ Returns the url to access a detail record for this offer."""
        return reverse('realtor',  kwargs={'pk': self.pk})
##==========================================================================
## SIGNALS FOR REALTOR
def delete_avatar(sender, instance, **kwargs):
    if instance.avatar:
        instance.avatar.delete(False)

models.signals.pre_delete.connect(delete_avatar, sender=Realtor)

def create_realtor(sender, **kwargs):
    if kwargs['created']:
        realtor = Realtor.objects.create(created_by=kwargs['instance'])

models.signals.post_save.connect(create_realtor, sender=User)

##===========================================================================
## FOR SAVING currency curses
class Dollar(models.Model):
    curse = models.DecimalField(max_digits=5, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return f"{self.curse} - {self.pub_date}"


class StatisticUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name="User")
    # RATING AND COUNTING OF OFFERS
    # rating = models.DecimalField(verbose_name='Рейтинг', max_digits=3,
    #         decimal_places=2, default=0.00)
    limit_offers = models.PositiveSmallIntegerField(
                 verbose_name='Ліміт оголошень, штук', default=1)
    offers = models.PositiveSmallIntegerField(
           verbose_name="Об'єктів на продаж", default=0)
    in_archive = models.PositiveSmallIntegerField(
               verbose_name="Об'єктів в архіві", default=0)
    def __str__(self) :
        return self.user
    class Meta:
        ordering = ["user"]


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
         verbose_name='User')
    payment = models.PositiveIntegerField(verbose_name="Сума оплати")
    currency = models.CharField(verbose_name='Валюта', max_length=3,
             choices=(('UAH', 'UAH'), ('USD', 'USD'), ('EUR', 'EUR')),
             blank=False, default='EUR',)
    pay_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.payment} {self.currency} - {self.pay_date} - {self.user}'
    class Meta:
        ordering = ["-id"]


class LeadGenerator(models.Model):
    phone = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    offer_type = models.CharField(max_length=50)
    offer_id = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-pub_date"]
    def __str__(self):
        return f'{self.phone} {self.name} {self.title}'
