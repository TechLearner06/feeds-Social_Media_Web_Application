# Generated by Django 5.0 on 2024-06-29 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_rename_followers_followerslist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
    ]