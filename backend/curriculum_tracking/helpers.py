from . import models
from core import models as core_models
from django.db.models import F
from backend.settings import REVIEW_SPAM_THRESHOLD
from django.db.models import Count, Subquery
from sql_util.utils import SubqueryAggregate
from django.db.models import Q


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
        # print(f"card for {project}")
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
    except models.AgileCard.DoesNotExist:
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


def agile_card_reviews_outstanding(user):
    """AgileCards that the user must review. These are cards that are in the review column that the user has not reviewed since the last review request time

    If a card already has REVIEW_SPAM_THRESHOLD reviews then exclude it from the returned array
    """
    cards = (
        models.AgileCard.objects.filter(reviewers__in=[user])
        .filter(status=models.AgileCard.IN_REVIEW)
        .filter(assignees__active=True)
        .annotate(
            recent_review_count=SubqueryAggregate(
                "recruit_project__project_reviews",
                aggregate=Count,
                filter=Q(timestamp__gte=F("recruit_project__review_request_time")),
            )
        )
        .filter(
            Q(recent_review_count__lt=REVIEW_SPAM_THRESHOLD)
            | Q(recent_review_count__isnull=True)
        )
    )

    reviews_done_by_user = (
        models.RecruitProjectReview.objects.filter(
            recruit_project__agile_card__status=models.AgileCard.IN_REVIEW
        )
        .filter(reviewer_user=user)
        .filter(recruit_project__review_request_time__lte=F("timestamp"))
        .prefetch_related("recruit_project__agile_card")
    )
    already_reviewed = [o.recruit_project.agile_card for o in reviews_done_by_user]

    return [card for card in cards if card not in already_reviewed]


def pull_request_reviews_outstanding(user):
    # TODO: only implement this once the github webhook is healthier
    return []
