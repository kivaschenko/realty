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
    address = models.CharField(max_length=255, verbose_name='Адреса', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
               related_name='agencys', verbose_name='Редактор сторінки',
               null=True,)
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
        super().save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        """ Returns the url to access a detail record for the agency.
        """
        return reverse('agency', kwargs={'slug': self.slug})


class Realtor(models.Model):
    """ Model represents all information about rieltor
    """
    phone = models.CharField(max_length=13, verbose_name="Телефон основний",
        help_text="міжнародний формат, +38067XXXYYZZ",)
    start_year = models.CharField(max_length=4,
        verbose_name='Рік початку роботи ріелтором')
    agensy = models.ForeignKey(Agency, on_delete=models.SET_NULL, related_name='realtors',
            null=True,  blank=True, verbose_name="Агенство",)
    bio = models.TextField(max_length=1000, blank=True, null=True,
        verbose_name="Подробиці про ріелтора",
        help_text="<em>все, що вважаєте за потрібне про себе, свою фірму до 1000 знаків</em>",)
    created_by = models.OneToOneField(User, on_delete=models.CASCADE,
               verbose_name='Власник профілю',)
    num_visits = models.PositiveIntegerField(default=0)
    # RATING AND COUNTING OF OFFERS
    rating = models.DecimalField(verbose_name='Рейтинг', max_digits=3,
            decimal_places=2, default=0.00)
    offers = models.PositiveSmallIntegerField(verbose_name="Об'єктів на продаж",
            default=0)
    in_archive = models.PositiveSmallIntegerField(
               verbose_name="Об'єктів в архіві", default=0)

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
        return f'{self.pk} {self.created_by.first_name} {self.created_by.last_name} - {self.agensy}'

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        """ Returns the url to access a detail record for this offer."""
        return reverse('realtor',  kwargs={'pk': self.pk})

CHOICE_SET = (
    ('5', '5- відмінно, Щиро рекомендую'),
    ('4', '4- добре, Рекомендую'),
    ('3', '3- задовільно, Утримуюсь від рекомендацій'),
    ('2', '2- погано, Не рекомендую'),
    ('1', '1- жахливо, Категорично не рекомендую'),
)
class Review(models.Model):
    """ Model represents the user's reviews about realtors
    """
    choice = models.CharField(max_length=1,
            verbose_name="Загальне враження від співпраці")
    rating = models.PositiveSmallIntegerField(default=0)
    message = models.TextField(max_length=2000, verbose_name="Відгук",
            help_text='до 2000 знаків')
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.created_at} - {self.created_by} оцінка: {self.choice} \
для {self.realtor}'


class Answer(models.Model):
    """Realtor says to the review only one time
    """
    title = models.CharField(max_length=50, verbose_name='Заголовок',
            default='Дякую за відгук')
    message = models.TextField(max_length=2000, verbose_name="Відповідь",
            help_text='до 2000 знаків')
    review = models.OneToOneField(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.created_at} - {self.title} - {self.review}'
