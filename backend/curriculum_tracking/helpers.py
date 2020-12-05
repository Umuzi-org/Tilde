# from git_real import helpers as git_helpers
from . import models

# from . import constants
# import re
from core import models as core_models
from collections import namedtuple


# def get_repo_full_name_from_url(url):
#     print(url)
#     repo_full_name_found = re.findall("https://github.com/(.*/.*)[\.git]*", url)
#     if not repo_full_name_found:
#         return
#     repo_full_name = repo_full_name_found[0].strip(".git")

#     # TODO: test??
#     return repo_full_name

# def get_full_url_from_content_link_param(url_template, url_part: str) -> str:

#     return url_template.format(url_part.strip("/"))

# cleaned = url_part.strip("/")
# if cleaned.startswith(constants.CURRICULUM_STATIC_SITE_URL):
#     cleaned = cleaned[len(constants.CURRICULUM_STATIC_SITE_URL) :]
# if cleaned.startswith("content/"):
#     cleaned = cleaned[len("content/") :]
# if cleaned.endswith("/_index.md"):
#     cleaned = cleaned[: -len("/_index.md")]
# cleaned = cleaned.strip("/")

# assert '"' not in url_part, f"invalid url part: {url_part}"

# result = constants.RAW_CONTENT_URL.format(
#     content_sub_dir=f"content/{cleaned}/_index.md"
# )

# assert (
#     result.count("https://") == 1
# ), f"url_part '{url_part}' results in invalid url: {result}"
# assert (
#     result.count("//") == 1
# ), f"url_part '{url_part}' results in invalid url: {result}"

# assert "content/content" not in result, f"{url_part} => {result}"

# assert "/content/" in result, f"{url_part} => {result}"

# return result


def get_projects(cohort=None, user=None):
    if user:
        for project in models.RecruitProject.objects.filter(recruit_users__in=[user]):
            yield project
    elif cohort:
        for user in cohort.get_member_users():
            for project in models.RecruitProject.objects.filter(
                recruit_users__in=[user]
            ):
                yield project
    else:

        for o in models.RecruitProject.objects.all():
            yield o


def generate_project_cards(cohort, user):
    # prune_projects()
    for project in get_projects(cohort, user):
        print(f"card for {project}")
        create_or_update_single_project_card(project)


def generate_repo_name_for_project(user, project, flavour_names):
    """when we create repos for recruit projects then we need names. for the repos. This creates those names"""
    clean_name = lambda s: "".join([c for c in s if c.isalnum()])
    slug = project.slug
    first_name = clean_name(user.first_name)
    last_name = clean_name(user.last_name)

    project_name = (
        f"{first_name}-{last_name}-{project.id}-{slug}-{'-'.join(flavour_names)}"
    )
    if len(project_name) > 100:

        diff = len(project_name) - 100
        slug = slug[:-diff]
        project_name = (
            f"{first_name}-{last_name}-{slug}-{project.id}-{'-'.join(flavour_names)}"
        )
        assert (
            len(project_name) == 100
        ), f"len({project_name}) ={len(project_name)}. Expected 100 "
    return project_name


def _get_or_create_flavoured_project(project_content_item, repo, flavour_names):

    recruit_projects = models.RecruitProject.objects.filter(
        content_item=project_content_item,
        repository=repo,
    )
    for project in recruit_projects:
        if project.flavours_match(flavour_names):
            return project
    project = models.RecruitProject.objects.create(
        content_item=project_content_item, repository=repo
    )

    project.set_flavours(flavour_names)
    return project


def save_newly_created_project_repo_to_db(
    github_auth_login, recruit_user, project_content_item, repo_full_name, flavour_names
):
    repo_dict = git_helpers.get_repo(
        github_auth_login=github_auth_login, repo_full_name=repo_full_name
    )

    repo = git_helpers.save_repo(
        repo_dict
    )  # note thet the repo itself doesn't "belong" to anyone

    recruit_project = _get_or_create_flavoured_project(
        project_content_item, repo, flavour_names
    )

    if recruit_user not in [o.id for o in recruit_project.recruit_users.all()]:
        recruit_project.recruit_users.add(recruit_user)
        recruit_project.save()
    return recruit_project


def create_recruit_project_for_submission_type_REPOSITORY(
    github_auth_login, recruit_user, project_content_item, flavour_names
):
    from social_auth import models as social_models
    from git_real.constants import ORGANISATION

    try:
        social = social_models.SocialProfile.objects.get(user=recruit_user)

    except social_models.SocialProfile.DoesNotExist:
        print(f"{recruit_user.id} {recruit_user}")
        raise
    github_name = social.github_name

    repo_name = generate_repo_name_for_project(
        recruit_user, project_content_item, flavour_names
    )

    repo_full_name = f"{ORGANISATION}/{repo_name}"
    readme_text = "\n".join(
        [
            f"{project_content_item.title} ({project_content_item.id})",
            f"For raw project instructions see: {project_content_item.url}",
        ]
    )

    git_helpers.create_repo_and_assign_contributer(
        github_auth_login,
        repo_full_name,
        github_user_name=github_name,
        readme_text=readme_text,
    )

    project = save_newly_created_project_repo_to_db(
        github_auth_login=github_auth_login,
        recruit_user=recruit_user,
        project_content_item=project_content_item,
        repo_full_name=repo_full_name,
        flavour_names=flavour_names,
    )

    assert project
    return project


def assert_users_same(card, project):
    card_assignees = sorted([o.id for o in card.assignees.all()])
    card_reviewers = sorted([o.id for o in card.reviewers.all()])
    project_reviewers = sorted([o.id for o in project.reviewer_users.all()])
    project_assignees = sorted([o.id for o in project.recruit_users.all()])

    assert card_assignees == project_assignees
    assert card_reviewers == project_reviewers


def create_or_update_single_project_card(project):
    try:
        card = project.agile_card
        print("card exists")
    except models.AgileCard.DoesNotExist:
        print("creating card")
        card = _create_card_from_project(project)

    assert card is not None
    update_card_from_project(card, project)
    assert_users_same(card, project)


def update_card_from_project(card, project):
    card.reviewers.set(project.reviewer_users.all())
    card.assignees.set(project.recruit_users.all())

    fresh_status = models.AgileCard.derive_status_from_project(project)
    card.status = fresh_status
    card.save()


def update_card_from_topic_progress(card, progress):
    fresh_status = models.AgileCard.derive_status_from_topic(progress, card)
    card.status = fresh_status
    card.save()


def _create_card_from_project(project):

    query = None
    for user in project.recruit_users.all():
        query = query or models.AgileCard.objects.filter(
            content_item=project.content_item,
            assignees__in=[user],
        )
    matching_cards = list(query)

    card_status = models.AgileCard.derive_status_from_project(project)

    # assert (
    #     project.latest_review_status == project.latest_trusted_review_status
    # ), "TODO: we need to fix this"

    if len(matching_cards) == 0:
        card = models.AgileCard.objects.create(
            content_item=project.content_item,
            status=card_status,
            recruit_project=project,
            is_hard_milestone=False,
            is_soft_milestone=False,
        )
        card.reviewers.set(project.reviewer_users.all())
        card.assignees.set(project.recruit_users.all())

        card.save()
        return card

    if len(matching_cards) == 1:
        # assert False, "noop"
        # branch not tested!!
        card = matching_cards[0]
        card.status = card_status
        card.recruit_project = project
        card.save()
        card.reviewers.set(project.reviewer_users.all())
        card.assignees.set(project.recruit_users.all())

        for user in card.reviewers.all():
            if user not in project.reviewer_users.all():
                card.reviewers.remove(user)
        for user in card.assignees.all():
            if user not in project.recruit_users.all():
                card.assignees.remove(user)

        return card

    raise Exception(f"too many matching cards: {matching_cards}")


def get_curriculums(cohort=None):
    if cohort:
        return [cohort.cohort_curriculum]
    return core_models.Curriculum.objects.all()
