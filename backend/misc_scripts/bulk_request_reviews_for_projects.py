"""basically, every IP project that has a submision time should be put into the in review column. Also if a project has reviewers then add them to the card"""

from curriculum_tracking.models import AgileCard
from core.models import Cohort

cards = AgileCard.objects.filter(status=AgileCard.IN_PROGRESS)
for card in cards:
    project = card.recruit_project
    if project:
        if project.complete_time:
            project.request_review(project.complete_time)
        for user in project.reviewer_users.all():
            card.reviewers.add(user)
    card.save()
    project.save()


# delete cards for inactive Cohorts

for cohort in Cohort.objects.all():
    if cohort.active == False or cohort.suppress_card_generation:
        for user in cohort.get_member_users:
            AgileCard.objects.filter(user=user).delete()
