from django.core.management.base import BaseCommand
from backend.settings import CURRICULUM_TRACKING_REVIEW_BOT_EMAIL
from core.models import User
from curriculum_tracking.models import AgileCard, RecruitProjectReview
from curriculum_tracking.constants import NOT_YET_COMPETENT, COMPETENT
from django.utils import timezone
import requests


def get_automark_result(repo_url, content_item_id, flavours):
    # print(repo_url)
    # print(content_item_id)
    # print(flavours)
    url = "http://localhost:1313/mark-project"
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        url,
        headers=headers,
        json={
            "repoUrl": repo_url,
            "contentItemId": content_item_id,
            "flavours": flavours,
        },
    )
    return response.json()


#     curl \
# --request POST \
# --header "Content-Type: application/json" \
# --data '{"repoUrl":"git@github.com:Umuzi-org/David-Chambers-273-simple-calculator-part-1-python.git","contentItemId":273, "flavours": ["python"]}' \
# http://localhost:1313/mark-project


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("content_item", type=str)
        parser.add_argument("flavours", type=str, default="")

    def add_review(self, card, status, comments):
        base_comments = "Hello! I'm a robot 🤖\n\nI'm here to give you quick feedback about your code."
        if status == COMPETENT:
            full_comments = f"{base_comments} {comments}"
        else:
            full_comments == f"{base_comments} I'm not very clever, I can't give you super detailed feedback. But I did notice that something is broken. Here's the error message I came up with:\n\n```{comments}```\n\nIf the feedback doesn't make sense please reach out to one of the humans that work here and they'll be happy to help you understand."
            breakpoint()
        RecruitProjectReview.objects.create(
            status=status,
            timestamp=timezone.now(),
            comments=full_comments,
            recruit_project=card.recruit_project,
            reviewer_user=self.bot_user,
        )

    def handle(self, *args, **options):
        content_item = options["content_item"]
        flavours = [s.strip() for s in options["flavours"].split(",") if s]

        self.bot_user, _ = User.objects.get_or_create(
            email=CURRICULUM_TRACKING_REVIEW_BOT_EMAIL
        )

        cards = (
            AgileCard.objects.filter(status=AgileCard.IN_REVIEW)
            .filter(content_item__title=content_item)
            .filter(assignees__active__in=[True])
        )

        for card in cards:
            if flavours and not card.flavours_match(flavours):
                continue

            has_review = (
                card.recruit_project.project_reviews.filter(
                    timestamp__gt=card.recruit_project.review_request_time
                )
                .filter(reviewer_user=self.bot_user)
                .count()
            )
            if has_review:
                continue

            print(card.assignees.all())

            result = get_automark_result(
                repo_url=card.recruit_project.repository.ssh_url,
                content_item_id=card.content_item_id,
                flavours=card.flavour_names,
            )
            if result["status"] == "OK":
                self.add_review(card=card, status=COMPETENT, comments=result["message"])
            elif result["status"] == "FAIL":
                self.add_review(
                    card=card, status=NOT_YET_COMPETENT, comments=result["message"]
                )
