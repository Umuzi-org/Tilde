"""
python manage.py export_reviews_for_poor_mans_trust_prop percival.rapha@umuzi.org "Validate a South African ID number" "python"

"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from curriculum_tracking.models import RecruitProjectReview, AgileCard

User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str)
        parser.add_argument("content_item_title", type=str)
        parser.add_argument("flavour", type=str)

    def handle(self, *args, **options):
        who = options["who"]
        content_item_title = options["content_item_title"]
        flavours = [s for s in options["flavour"].split(",") if s]

        user = User.objects.get(email=who)
        reviews = (
            RecruitProjectReview.objects.filter(
                reviewer_user=user,
                recruit_project__content_item__title=content_item_title,
            )
            .order_by("-timestamp")
            .prefetch_related("recruit_project")
        )

        final = set()
        for review in reviews:
            project = review.recruit_project
            if project.flavours_match(flavours):
                try:
                    card = project.agile_card
                except AgileCard.DoesNotExist:
                    pass
                else:
                    final.add(card.id)
                    if len(final) > 10:
                        break

        print(
            f""" 
# Docs


See "Poor Man's trust prop" docs here: https://app.gitbook.com/o/2DzlYnPstQTFtiSgav55/s/QrgdShfgwVxn9oBO7tlc/reviewing-learner-projects/poor-mans-trust-propagation


# Nomination under review  


{who}
{content_item_title}
{', '.join(flavours)}    


# Reviews to be considered


"""
        )

        for card_id in final:
            print(
                f"\nhttps://tilde-front-dot-umuzi-prod.nw.r.appspot.com/card/{card_id}"
            )
