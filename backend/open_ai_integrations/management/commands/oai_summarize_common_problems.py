import os
import openai
from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProjectReview, RecruitProject
from core.models import User
from django.utils import timezone
from curriculum_tracking.constants import (
    NEGATIVE_REVIEW_STATUS_CHOICES,
    NOT_YET_COMPETENT,
)

openai.api_key = os.getenv("OPENAI_API_KEY")  # TODO: rather put in settings file


REVIEWERS = [
    # "Staff Tech Education",
    "sheena.oconnell@umuzi.org",
    # "ruddy.riba@umuzi.org",
    # "vuyisanani.meteni@umuzi.org",
]

cutoff_days = 90
cutoff_number_of_reviews = 3


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("title", type=str)
        parser.add_argument("flavours", type=str)

    def get_review_comments(self, title, flavours):
        reviewers = []
        for who in REVIEWERS:
            reviewers.extend(User.get_users_from_identifier(who))

        reviews = (
            RecruitProjectReview.objects.filter(reviewer_user__email__in=reviewers)
            .filter(
                timestamp__gte=timezone.now() - timezone.timedelta(days=cutoff_days)
            )
            .filter(recruit_project__content_item__title=title)
            .filter(status=NOT_YET_COMPETENT)
            .order_by("-timestamp")
            .prefetch_related("recruit_project")
        )

        comments = []
        for review in reviews:
            if len(comments) == cutoff_number_of_reviews:
                break
            if sorted(review.recruit_project.flavour_names) != flavours:
                continue
            comments.append(review.comments)

        return comments

    def generate_chat_prompt(self, comments):
        """This prompt is good for chatGPT"""
        joined_comments = "\n\nNext review:\n\n".join(comments)
        return f"Learners at a code school submit code to be reviewed.  I will supply some reviews that were left by markers.   Please tell me the most common problems highlighted by the reviews. \n\nFirst review:\n\n {joined_comments}"

    def generate_prompt(self, comments):

        joined_comments = "\n\n".join(comments)
        return f"Here is feedback given on some student projects:\n\n{joined_comments}.\n\n :"

    def handle(self, *args, **options):
        title = options["title"]
        flavours = sorted(options["flavours"].split(","))

        comments = self.get_review_comments(title, flavours)
        if len(comments) == 0:
            print("No matching reviews")
            return

        prompt = self.generate_chat_prompt(comments)
        print(f"CHAT PROMPT\n=======\n\n{prompt}\n\n=======")

        breakpoint()

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
        )

        breakpoint()

        foo
