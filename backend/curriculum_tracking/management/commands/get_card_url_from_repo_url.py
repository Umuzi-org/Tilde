from django.core.management.base import BaseCommand
from git_real.models import Repository
from curriculum_tracking.models import AgileCard
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("url", type=str)

    def handle(self, *args, **options):
        url = options["url"]

        repo = Repository.objects.get(ssh_url=url)
        projects = repo.recruit_projects.all()

        cards = [
            AgileCard.objects.filter(recruit_project=project).first()
            for project in projects
        ]

        cards = [card for card in cards if card is not None]

        for card in cards:
            print(f"https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/card/{card.id}")
