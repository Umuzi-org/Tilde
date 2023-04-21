from core.models import *
from curriculum_tracking.models import *
from django.db.models import Q
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User

# sololearn python content

content_ids = [
    748,
    749,
    752,
    745,
]

whitelist = [
    "cohort",
    "foundation 2",
    "foundation 3",
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        projects = RecruitProject.objects.filter(
            content_item_id__in=content_ids
        ).filter(complete_time__isnull=False)
        by_assignee = {}

        for project in projects:
            assignee_id = project.recruit_users.first().id
            by_assignee[assignee_id] = by_assignee.get(assignee_id, [])
            by_assignee[assignee_id].append(project)

        by_assignee_complete_only = {
            assignee_id: projects
            for (assignee_id, projects) in by_assignee.items()
            if len(projects) == 4
        }

        final_assignees = []

        skip_users = []

        for user in User.objects.filter(pk__in=by_assignee_complete_only.keys()):
            team_names = "\n".join([o.name.lower() for o in user.teams()])
            appended = False
            for s in whitelist:
                if s in team_names:
                    final_assignees.append(user)
                    appended = True
                    break
            if not appended:
                skip_users.append(user)

        final_assignee_ids = [o.id for o in final_assignees]

        by_assignee_complete_only_good_users = {
            assignee_id: projects
            for (assignee_id, projects) in by_assignee_complete_only.items()
            if assignee_id in final_assignee_ids
        }

        durations = []

        for projects in by_assignee_complete_only_good_users.values():
            duration = 0
            for project in projects:
                duration += (project.complete_time - project.start_time).total_seconds()
            durations.append(duration)

        durations.sort()
        nice_durations = [timezone.timedelta(seconds=x) for x in durations]

        minimum = min(nice_durations)
        maximum = max(nice_durations)
        mean = timezone.timedelta(seconds=sum(durations) / len(durations))

        print(f"minimum = {minimum}")
        print(f"maximum = {maximum}")
        print(f"mean = {mean}")
