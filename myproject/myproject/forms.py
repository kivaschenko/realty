from django import forms

SUBJECTS = [
    ('[ Повідомлення із сайту ] Проблема з аккаунтом', 'Проблема з аккаунтом'),
    ('[ Повідомлення із сайту ] Поскаржитись на оголошення або коментар',
     'Поскаржитись на оголошення або коментар'),
    ('[ Повідомлення із сайту ] Пропозиція по рекламі на сайті', 'Пропозиція по рекламі на сайті'),
    ('[ Повідомлення із сайту ] Інші питання', 'Інші питання'),
]

class ContactForm(forms.Form):
    subject = forms.ChoiceField(choices=SUBJECTS, label='Тема')
    message = forms.CharField(
            widget=forms.Textarea(attrs={'rows':5}),
            label='Текст')
    email = forms.EmailField(label='Email для відповіді')
    cc_myself = forms.BooleanField(required=True, label='Надіслати копію собі')
