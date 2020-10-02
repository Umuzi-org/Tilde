""" These helper functions were leveraged heavily in preparing the recruit projects for flavoursome cards.
There were a lot of different messes to be cleaned up
"""

from taggit.models import Tag
import csv
from core.models import Cohort, RecruitCohort, User, UserGroup
from curriculum_tracking.models import (
    RecruitProject,
    ContentItem,
    AgileCard,
    CurriculumContentRequirement,
)


javascript = Tag.objects.get_or_create(name="javascript")[0]
python = Tag.objects.get_or_create(name="python")[0]
java = Tag.objects.get_or_create(name="java")[0]
kotlin = Tag.objects.get_or_create(name="kotlin")[0]
swift = Tag.objects.get_or_create(name="swift")[0]
typescript = Tag.objects.get_or_create(name="typescript")[0]
none = Tag.objects.get_or_create(name="none")[0]


def get_project_info(content_item_id, user_id):
    user = User.objects.get(pk=user_id)
    projects = RecruitProject.objects.filter(
        content_item_id=content_item_id, recruit_users__in=[user]
    )
    groups = UserGroup.objects.filter(users__in=[user])
    cohorts = [o.cohort for o in RecruitCohort.objects.filter(user=user)]
    content_item = ContentItem.objects.get(pk=content_item_id)
    print(f"user = {user}")
    print(f"groups = {groups}")
    print(f"cohorts = {cohorts}")
    print(f"content_item = {content_item}")
    print(f"{projects.count()} matching projects:")
    for project in projects:
        print(f"Project: id={project.id} {project}")
        print(f"\trepo: {project.repository.ssh_url}")
        try:
            print(f"\tcard: id={project.agile_card.id} {project.agile_card}")
        except AgileCard.DoesNotExist:
            print("\tno card")
    print()


def export_projects_without_flavours():
    with open("gitignore/projects_needing_flavours.csv", "w") as f:
        writer = csv.writer(f)
        for project in RecruitProject.objects.all():
            if project.flavours.count() == 0:
                all_groups = []
                for user in project.recruit_users.all():
                    all_groups.extend(
                        [
                            f"group {o.id} {o.name}"
                            for o in UserGroup.objects.filter(users__in=[user])
                        ]
                    )
                    all_groups.extend(
                        [
                            f"c {o.id} {o.cohort.label}"
                            for o in RecruitCohort.objects.filter(user=user)
                        ]
                    )
                writer.writerow(
                    [
                        project.id,
                        str(project),
                        set(all_groups),
                        project.repository.ssh_url if project.repository else "",
                        [o.name for o in project.content_item.available_flavours.all()],
                    ]
                )


def assign_flavours_to_cohort(cohort_id, default_flavour):
    cohort = Cohort.objects.get(pk=cohort_id)
    users = [o.user for o in RecruitCohort.objects.filter(cohort=cohort)]
    for user in users:
        assign_flavours_to_user(user, default_flavour)


def assign_flavours_to_user(user, default_flavour):
    for project in RecruitProject.objects.filter(recruit_users__in=[user]):
        if project.flavours.count() > 0:
            continue
        available_flavours = project.content_item.available_flavours.all()
        if default_flavour in available_flavours:
            print(f"project: {project.id} {project}")
            project.flavours.add(default_flavour)


def assign_flavours_to_user_by_email(email, default_flavour):
    user = User.objects.get(email=email)
    assign_flavours_to_user(user, default_flavour)


def remove_flavours(cohort_id):
    cohort = Cohort.objects.get(pk=cohort_id)
    users = [o.user for o in RecruitCohort.objects.filter(cohort=cohort)]
    for user in users:
        for project in RecruitProject.objects.filter(recruit_users__in=[user]):
            project.flavours.clear()
            print(project)
            print(project.flavours)


def export_project_flavours(cohort_id):
    cohort = Cohort.objects.get(pk=cohort_id)
    users = [o.user for o in RecruitCohort.objects.filter(cohort=cohort)]
    all_projects = []
    for user in users:
        all_projects.extend(RecruitProject.objects.filter(recruit_users__in=[user]))
    all_projects.sort(
        key=lambda project: (
            [o.id for o in project.recruit_users.all()],
            project.content_item_id,
        )
    )
    with open(f"gitignore/cohort_projects_{cohort_id}_{cohort.label}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "project.id",
                "content_item",
                "repository.full_name",
                "project.flavours",
                "content_item.available_flavours",
            ]
        )
        for project in all_projects:
            writer.writerow(
                [
                    project.id,
                    project.content_item,
                    project.repository.full_name,
                    [o.name for o in project.flavours.all()],
                    [o.name for o in project.content_item.available_flavours.all()],
                ]
            )


def if_one_flavour_available_then_assign(cohort_id=None):

    cohort = Cohort.objects.get(pk=cohort_id)
    users = [o.user for o in RecruitCohort.objects.filter(cohort=cohort)]
    for user in users:
        for project in RecruitProject.objects.filter(recruit_users__in=[user]):
            if project.flavours.count() > 0:
                continue
            if project.content_item.available_flavours.count() == 1:
                flavour = project.content_item.available_flavours.first()
                if flavour != none:
                    print(f"adding {flavour.name} to {project}")
                    project.flavours.add(flavour)


def change_project_flavour(project_id, to):
    project = RecruitProject.objects.get(pk=project_id)
    project.flavours.clear()
    project.flavours.add(to)


def export_nosubmit_projects():
    with open("gitignore/nosubmit_projects.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["project.id", "project.content_item_id", "project.content_item.title"]
        )
        for project in RecruitProject.objects.filter(
            content_item__project_submission_type=ContentItem.NO_SUBMIT
        ).order_by("content_item_id"):
            writer.writerow(
                [project.id, project.content_item_id, project.content_item.title]
            )


def change_project_content_item_id(from_id, to_id):
    print(f"from {ContentItem.objects.get(pk=from_id)}")
    print(f"to {ContentItem.objects.get(pk=to_id)}")
    for project in RecruitProject.objects.filter(content_item_id=from_id):
        print(project.id)
        project.content_item_id = to_id
        project.save()
    print()


def get_project_info(content_item_id, user_id):
    user = User.objects.get(pk=user_id)
    projects = RecruitProject.objects.filter(
        content_item_id=content_item_id, recruit_users__in=[user]
    )
    if projects.count() < 2:
        return
    flavours = [
        sorted([o.name for o in project.flavours.all()]) for project in projects
    ]
    flavours = [",".join(l) for l in flavours]
    if len(set(flavours)) == projects.count():
        return
    groups = UserGroup.objects.filter(users__in=[user])
    cohorts = [o.cohort for o in RecruitCohort.objects.filter(user=user)]
    content_item = ContentItem.objects.get(pk=content_item_id)
    print(f"user = {user}")
    print(f"groups = {groups}")
    print(f"cohorts = {cohorts}")
    print(f"content_item = {content_item}")
    print(f"{projects.count()} matching projects:")
    for project in projects:
        print(f"Project: id={project.id} {project}")
        print(f"\trepo: {project.repository.ssh_url}")
        print(f"\tflavours: {[o.name for o in project.flavours.all()]}")
        try:
            print(f"\tcard: id={project.agile_card.id} {project.agile_card}")
        except AgileCard.DoesNotExist:
            print("\tno card")
    print()


SQL_QUERY_TO_FETCH_POTENTIAL_DUPLICATE_PROJECTS = """
select  count(*) ,curriculum_tracking_recruitproject.content_item_id,curriculum_tracking_recruitproject_recruit_users.user_id 
into TEMPORARY temp
from curriculum_tracking_recruitproject, curriculum_tracking_recruitproject_recruit_users where curriculum_tracking_recruitproject_recruit_users.recruitproject_id = curriculum_tracking_recruitproject.id group by user_id,content_item_id;
select * from temp where count>1;
"""


def change_content_id(project_id, cid, flavour):
    o = RecruitProject.objects.get(pk=project_id)
    o.content_item_id = cid
    o.save()
    o.flavours.add(flavour)


def pproject(id):
    proj = RecruitProject.objects.get(pk=id)
    print(proj)
    print(proj.repository)


def delete_nosubmit_instances():
    AgileCard.objects.filter(
        content_item__project_submission_type=ContentItem.NO_SUBMIT
    ).delete()
    CurriculumContentRequirement.objects.filter(
        content_item__project_submission_type=ContentItem.NO_SUBMIT
    ).delete()
    RecruitProject.objects.filter(
        content_item__project_submission_type=ContentItem.NO_SUBMIT
    ).delete()


def get_all_recruits_in_cohorts_with_matching_curriculum(curriculum_id):
    ds_users = []
    for cohort in Cohort.objects.filter(cohort_curriculum_id=2, active=True):
        if cohort.cohort_number == 22:
            continue
        for o in RecruitCohort.objects.filter(cohort=cohort, user__active=True):
            ds_users.append(o.user)
    return ds_users