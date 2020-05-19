# Generated by Django 3.0.4 on 2020-05-16 00:21

from django.conf import settings
from django.db import migrations, models
import root.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('root', '0007_auto_20200516_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='WhatsNew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('send_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=models.SET(root.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['send_date'],
            },
        ),
    ]
