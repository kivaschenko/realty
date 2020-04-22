from django import forms

SUBJECTS = [
    ('[ Повідомлення із сайту ] Проблема з аккаунтом', 'Проблема з аккаунтом'),
    ('[ Повідомлення із сайту ] Поскаржитись на оголошення', 'Поскаржитись на оголошення'),
    ('[ Повідомлення із сайту ] Пропозиція по рекламі на сайті', 'Пропозиція по рекламі'),
    ('[ Повідомлення із сайту ] Хочу такий сайт для агенції', 'Хочу такий сайт для агенції'),
    ('[ Повідомлення із сайту ] Інші питання', 'Інші питання'),
]

class ContactForm(forms.Form):
    subject = forms.ChoiceField(choices=SUBJECTS, label='Тема')
    message = forms.CharField(
            widget=forms.Textarea(attrs={'rows':7}),
            label='Текст')
    email = forms.EmailField(label='Email для відповіді')
    cc_myself = forms.BooleanField(required=False, label='Надіслати копію собі')
