# Generated by Django 5.0 on 2024-06-03 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_profile_id_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='id_user',
        ),
    ]
