# python manage.py propogate_staff_trust "Staff Tech Education"


from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q
from curriculum_tracking.models import RecruitProjectReview, AgileCard, ReviewTrust
from core.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who")

    def handle(self, *args, **options):
        who = options["who"]
        users = User.get_users_from_identifier(who)

        total = len(users)
        for i, user in enumerate(users):
            print(f"{i+1}/{total}: {user.email}")
            reviews = (
                RecruitProjectReview.objects.filter(reviewer_user=user)
                .filter(
                    Q(recruit_project__agile_card__status=AgileCard.COMPLETE)
                    | Q(recruit_project__agile_card__status=AgileCard.REVIEW_FEEDBACK)
                )
                .filter(trusted=False)
                .order_by("-timestamp")
                .prefetch_related("recruit_project")
            )

            performance = {}
            for review in reviews:
                key = f"{review.recruit_project.content_item.title} {review.recruit_project.flavour_names}"

                performance[key] = performance.get(
                    key,
                    {
                        "content_item_title": review.recruit_project.content_item.title,
                        "flavours": review.recruit_project.flavour_names,
                        "validated": [],
                    },
                )

                performance[key]["validated"].append(review.validated or "0")

            # reviewed at least REVIEWS_DONE projects of this type
            REVIEWS_DONE = 10

            performance = {
                k: v
                for (k, v) in performance.items()
                if len(v["validated"]) > REVIEWS_DONE
            }

            performance = {
                k: v
                for (k, v) in performance.items()
                if RecruitProjectReview.INCORRECT not in v["validated"][:8]
            }

            performance = {
                k: v
                for (k, v) in performance.items()
                if RecruitProjectReview.CONTRADICTED not in v["validated"][:3]
            }

            for k, v in performance.items():
                print(k)
                ReviewTrust.add_specific_trust_instances(
                    who=user.email,
                    content_item_title=v["content_item_title"],
                    flavours=v["flavours"],
                    update_previous_reviews=True,
                )
