# Generated by Django 3.0.4 on 2020-04-16 20:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import workspace.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workspace', '0002_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='workspace',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='room',
            name='slug',
            field=models.SlugField(default='Aa', verbose_name='slug'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workspace',
            name='slug',
            field=models.SlugField(default='Vvv', verbose_name='slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=models.SET(workspace.models.get_sentinel_user), to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace.Room', verbose_name='room'),
        ),
        migrations.AlterField(
            model_name='message',
            name='send_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='send_date'),
        ),
        migrations.AlterField(
            model_name='message',
            name='workspace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace.Workspace', verbose_name='workspace'),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=30, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='users'),
        ),
        migrations.AlterField(
            model_name='room',
            name='workspace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace.Workspace', verbose_name='workspace'),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='name'),
        ),
        migrations.AddConstraint(
            model_name='room',
            constraint=models.UniqueConstraint(fields=('workspace', 'name'), name='unique_room_ws'),
        ),
    ]
