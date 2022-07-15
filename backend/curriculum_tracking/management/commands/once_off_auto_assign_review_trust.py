# from django.core.management.base import BaseCommand
# from core.models import User
# from curriculum_tracking.models import ContentItem, RecruitProjectReview, ReviewTrust
# from backend.settings import (
#     CURRICULUM_TRACKING_TRUST_STREAK_LENGTH,
# )


# class Command(BaseCommand):
#     def get_latest_reviews(self, user):
#         content_items = (
#             ContentItem.objects.filter(projects__project_reviews__reviewer_user=user)
#             .filter(projects__project_reviews__validated=RecruitProjectReview.CORRECT)
#             .distinct()
#         )

#         for content_item in content_items:
#             # print(f"content_item = {content_item} [{content_item.id}]")
#             reviews = RecruitProjectReview.objects.filter(
#                 recruit_project__content_item=content_item, reviewer_user=user
#             ).order_by("-timestamp")

#             seen = []
#             for review in reviews:
#                 # print(review.recruit_project)
#                 flavours = ",".join(sorted(review.recruit_project.flavour_names))
#                 if flavours in seen:
#                     # print("seen")
#                     continue
#                 seen.append(flavours)
#                 yield review

#     def handle(self, *args, **options):

#         # team = Team.objects.get(name="Tech Junior Staff")
#         # users = team.user_set.all()

#         users = User.objects.filter(active=True)
#         for user in users:
#             print(user)
#             # user.save()
#             reviews = self.get_latest_reviews(user)
#             for review in reviews:
#                 if (
#                     review.get_validated_streak()
#                     >= CURRICULUM_TRACKING_TRUST_STREAK_LENGTH
#                 ):
#                     # print("trust earned!")
#                     ReviewTrust.add_specific_trust_instances(
#                         who=user.email,
#                         content_item_title=review.recruit_project.content_item.title,
#                         flavours=review.recruit_project.flavour_names,
#                         update_previous_reviews=True,
#                     )
#                     print(
#                         f"{review.recruit_project.content_item} {review.recruit_project.flavour_names} - {review.get_validated_streak()}"
#                     )
#             print()
