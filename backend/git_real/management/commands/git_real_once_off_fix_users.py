from git_real.models import PullRequest, Push, PullRequestReview, Commit
from git_real.helpers import get_user_from_github_name

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):

        # PRs

        prs = PullRequest.objects.filter(user__isnull=True)

        total_prs = prs.count()

        for i, pr in enumerate(prs):
            print(f"PR {i+1} / {total_prs}: [{pr.id}] {pr}")
            pr.user = get_user_from_github_name(pr.author_github_name)
            pr.save()

        # Pushes

        pushes = Push.objects.filter(user__isnull=True)

        total_pushes = pushes.count()

        for i, push in enumerate(pushes):
            print(f"Push {i+1} / {total_pushes}: [{push.id}] {push}")
            push.user = get_user_from_github_name(push.pusher_username)
            push.save()

        # PR reviews

        reviews = PullRequestReview.objects.filter(user__isnull=True)
        total = reviews.count()

        for i, o in enumerate(reviews):
            print(f"Review {i+1} / {total}: [{o.id}] {o}")
            o.user = get_user_from_github_name(o.author_github_name)
            o.save()

        # Commits
        commits = Commit.objects.filter(user__isnull=True)
        total = reviews.count()

        for i, o in enumerate(commits):
            print(f"Commit {i+1} / {total}: [{o.id}] {o}")
            o.user = get_user_from_github_name(o.author_github_name)
            o.save()
