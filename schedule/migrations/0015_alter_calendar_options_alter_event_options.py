# Generated by Django 4.2 on 2024-06-19 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0014_use_autofields_for_pk'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calendar',
            options={'verbose_name': 'календарь', 'verbose_name_plural': 'календари'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'событие', 'verbose_name_plural': 'события'},
        ),
    ]
