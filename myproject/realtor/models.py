from django.db import models

# Create your models here.
from django.contrib.auth.models import User


# Create your models here.
class Realtor(models.Model):
    """ Model represents all information about rieltor
    """
    phone = models.CharField(max_length=13, verbose_name="Телефон основний",
        help_text="міжнародний формат, +38067XXXYYZZ",)
    start_year = models.CharField(max_length=4,
        verbose_name='Рік початку роботи ріелтором')
    agensy = models.CharField(max_length=50, blank=True, null=True,
        verbose_name="Агенство, компанія", help_text="назва компанії, в якії працюєте",)
    bio = models.TextField(max_length=1000, blank=True, null=True,
        verbose_name="Подробиці про ріелтора",
        help_text="все, що вважаєте за потрібне про себе, свою фірму до 1000 знаків",)
    # ADDRESS
    address = models.CharField(max_length=155, verbose_name='Адреса офісу')
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
        return f'{self.created_by.first_name} {self.created_by.last_name} - {self.agensy}'

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
