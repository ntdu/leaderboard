from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.comment.models import Comment


class Command(BaseCommand):
    help = 'Seed the database with comments'

    def handle(self, *args, **kwargs):
        COMMENTS_COUNT = 55

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            email='email@gmail.com',
            defaults={'user_name': 'testuser', 'password': 'password'}
        )

        self.stdout.write(self.style.SUCCESS(F'Successfully seeded {COMMENTS_COUNT} comments into the database'))