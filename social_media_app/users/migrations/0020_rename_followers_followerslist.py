# Generated by Django 5.0 on 2024-06-29 16:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_post_location_post_video_alter_post_image_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Followers',
            new_name='FollowersList',
        ),
    ]
