from django.core.management.base import BaseCommand

# from core.models import User
from social_auth.models import SocialProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        count = (
            SocialProfile.objects.filter(user__active=True)
            .filter(github_name__isnull=False)
            .count()
        )
        print(f"Active users: {count}")
