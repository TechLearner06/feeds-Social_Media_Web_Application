from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Drops the users_followers table if it exists'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS users_followers')
        self.stdout.write(self.style.SUCCESS('Successfully dropped the users_followers table'))
