# Generated by Django 3.0.4 on 2020-04-16 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0003_auto_20200416_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='slug'),
        ),
    ]
