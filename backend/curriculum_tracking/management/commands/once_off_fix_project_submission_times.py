from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProject,AgileCard,RecruitProjectReview
from curriculum_tracking.constants import REVIEW_STATUS_CHOICES

class Command(BaseCommand):
    def handle(self, *args, **options):
        for project in RecruitProject.objects.all().prefetch_related("project_reviews"):
            print(project)
            project.complete_time = None 
            latest = project.latest_review(trusted=True) 
            if latest: 
                if latest.status in [COMPETENT,EXCELLENT]:
                    project.complete_time = latest.timestamp 
            project.start_time = project.start_time or project.repository.created_at 
            project.save() 


     





for o in RecruitCohort.objects.all():
    org = Organisation.objects.get(name = o.employer_partner.name)
    profile = UserProfile.objects.get_or_create(user=o.user)[0]
    if org.name in ["Umuzi","Code Club NG"]:
        profile.school_organisation = org 
    else:
        profile.sponsor_organisation = org 
    profile.save()



for org in Organisation.objects.order_by("name"):
    print(f"[{org.id}] {org.name}")

fix names