# Generated by Django 5.0 on 2024-06-26 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='username',
        ),
    ]
