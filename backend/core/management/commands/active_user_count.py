from django.core.management.base import BaseCommand
from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        count = User.objects.filter(active=True).count()
        print(f"Active users: {count}")
