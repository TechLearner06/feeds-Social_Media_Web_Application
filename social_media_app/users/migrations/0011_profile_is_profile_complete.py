# Generated by Django 5.0 on 2024-06-21 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_profile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_profile_complete',
            field=models.BooleanField(default=False),
        ),
    ]
