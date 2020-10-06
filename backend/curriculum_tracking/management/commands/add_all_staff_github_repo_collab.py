from core.models import User, Cohort, RecruitCohort
from curriculum_tracking.models import Cohort, RecruitProject
from social_auth.models import SocialProfile
from git_real.helpers import add_collaborator
from social_auth.github_api import Api
from git_real.constants import PERSONAL_GITHUB_NAME, ORGANISATION


staff_github_names = [
    o.github_name
    for o in SocialProfile.objects.filter(user__is_staff=True, user__active=True)
]

api = Api(PERSONAL_GITHUB_NAME)

cohort_ds = Cohort.objects.get(pk=50)
cohort_web = Cohort.objects.get(pk=51)
cohorts = [cohort_ds, cohort_web]
cohort_users = []

for cohort in cohorts:
    cohort_users.extend([o.user for o in RecruitCohort.objects.filter(cohort=cohort)])

projects = []
for user in cohort_users:
    projects.extend(RecruitProject.objects.filter(recruit_users__in=[user]))

repos = [project.repository for project in projects if project.repository]
repo_names = [
    repo.full_name for repo in repos if repo.full_name.startswith(ORGANISATION)
]

staff_count = len(staff_github_names)
repo_count = len(repo_names)

for repo_number, repo_full_name in enumerate(repo_names):
    print(f"Repo [{repo_number}/{repo_count}]: {repo_full_name}")
    for staff_number, github_user_name in enumerate(staff_github_names):
        print(f"\t adding user [{staff_number}/{staff_count}]: {github_user_name}")
        add_collaborator(api, repo_full_name, github_user_name)
