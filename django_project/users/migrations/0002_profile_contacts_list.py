# Generated by Django 3.1.2 on 2020-11-19 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='contacts_list',
            field=models.TextField(default='NO CONTACTS'),
        ),
    ]
