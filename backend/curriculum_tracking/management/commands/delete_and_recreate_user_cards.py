from django.core.management.base import BaseCommand
from curriculum_tracking import models, helpers
from core import models as core_models
from django.contrib.auth import get_user_model
from curriculum_tracking.card_generation_helpers import (
    generate_and_update_all_cards_for_user,
)

User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str)

    def handle(self, *args, **options):
        user = None
        who = options["who"]
        if who:
            if "@" in who:
                user = User.objects.get(email=who)
                models.AgileCard.objects.filter(assignees__in=[user]).delete()
                generate_and_update_all_cards_for_user(user, None)

            else:
                user_group = core_models.UserGroup.objects.get(name=who)
                # generate_all_content_cards_for_user_group(user_group)
                for o in core_models.UserGroupMembership.objects.filter(
                    group=user_group, permission_student=True
                ):
                    user = o.user
                    models.AgileCard.objects.filter(assignees__in=[user]).delete()
                    generate_and_update_all_cards_for_user(user, None)


# staff_cohort


# for user in User.objects.filter(is_staff=True, active=True):
#     reg = RecruitCohort.objects.get_or_create(
#         user=user,
#         defaults={
#             "employer_partner_id": 4,
#             "cohort": staff_cohort,
#             "start_date": now,
#             "end_date": now,
#         },
#     )[0]
#     reg.cohort = staff_cohort
#     reg.save()


# for cohort in Cohort.objects.all():
#     print(cohort)
#     for o in RecruitCohort.objects.filter(user__active=True,cohort=cohort):
#         print(o.user.email)
#     print()

# free_trial_cohort = Cohort.objects.create(
#     cohort_number=100,
#     cohort_curriculum_id=34,
#     start_date=now,
#     end_date=now,
# )

# for email in [
# "donnelly.keanonleon977@gmail.com",
# "thatotukisi23@gmail.com",
# "keigh2dah@gmail.com",
# "dario.dasilva@umuzi.org",]:
#     user = User.objects.get(email=email)
#     # CourseRegistration.objects.create(
#     # curriculum_id=34,
#     # order=2,
#     # user=user
#     # )
#     reg = RecruitCohort.objects.get_or_create(
#         user=user,
#         defaults={
#             "employer_partner_id": 4,
#             "cohort": free_trial_cohort,
#             "start_date": now,
#             "end_date": now,
#         },
#     )[0]
#     reg.cohort = free_trial_cohort
#     reg.save()
