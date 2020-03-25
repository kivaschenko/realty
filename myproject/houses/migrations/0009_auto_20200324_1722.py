# Generated by Django 2.2.7 on 2020-03-24 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0008_auto_20200324_1651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='Architecture',
        ),
        migrations.RemoveField(
            model_name='house',
            name='MSZoning',
        ),
        migrations.AlterField(
            model_name='house',
            name='MSSubClass',
            field=models.CharField(choices=[('20', '1-поверховий після 2000р., всі стилі'), ('30', '1-поверховий до 1999р.'), ('40', '1-поверх + мансарда, Незакінчений всі роки'), ('50', '1-поверх + мансарда, Закінчений всі роки'), ('60', '2-поверховий після 2000р.'), ('70', '2-поверховий до 1999р.'), ('75', '2-поверховий + мансарда всі роки'), ('80', 'Багаторівневий'), ('90', 'Кількаповерховий з фойе'), ('110', 'Дуплекс, Таунхаус - усі стилі після 2010р.'), ('120', '1-поврховий типовий радянський проект після 1960р.'), ('150', "на 2 сім'ї - типовий радянський проект")], default='20', help_text='Визначає тип житла, що бере участь у продажу', max_length=3, verbose_name="Тип об'єкта"),
        ),
    ]
