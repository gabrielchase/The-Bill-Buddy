# Generated by Django 2.0.1 on 2018-01-15 08:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bills',
            new_name='Bill',
        ),
    ]
