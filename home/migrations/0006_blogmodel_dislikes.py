# Generated by Django 4.0.3 on 2022-03-07 11:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0005_blogcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogmodel',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='dislikes', to=settings.AUTH_USER_MODEL),
        ),
    ]
