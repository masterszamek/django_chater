# Generated by Django 3.0.4 on 2020-05-15 23:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0004_auto_20200514_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='ideas_container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='root.IdeasContainer', verbose_name='priority'),
        ),
    ]
