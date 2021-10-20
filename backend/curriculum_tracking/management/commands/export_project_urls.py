from django.core.management.base import BaseCommand
from core.models import Team
from curriculum_tracking.models import RecruitProject
import csv

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("team_name", type=str)
        parser.add_argument("content_item_title", type=str)

    def handle(self, *args, **options):
        print(args, options)
        team = Team.objects.get(name=options["team_name"])
        results = get_email_and_url(team)

        with open('gitignore/test.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['user_eamil', 'url'])
            writer.writerows(results)

def get_email_and_url(team):
    results = []
    for user in team.active_users:
        project = RecruitProject.objects.filter(content_item__title=options['content_item_title']).filter_by(recruit_users__in=[user]).first()
        # results.append([user.email, project.link_submission if project else None])# if prject not completed - just leave it blank or add none
        results.append([user.email, project and (project.link_submission or project.git_url)])
    return results
