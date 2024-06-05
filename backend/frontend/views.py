import json
from functools import wraps
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.core.signing import SignatureExpired, BadSignature
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, login, logout
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.contrib.contenttypes.models import ContentType
from activity_log.models import LogEntry

from core.models import Team
from curriculum_tracking.models import (
    AgileCard,
    ContentItem,
    User,
    RecruitProject,
    TopicProgress,
    RecruitProjectReview,
)

import curriculum_tracking.activity_log_entry_creators as log_creators
from curriculum_tracking import helpers

from taggit.models import Tag
from guardian.core import ObjectPermissionChecker

from threadlocal_middleware import get_current_request

from .forms import (
    ForgotPasswordForm,
    CustomAuthenticationForm,
    CustomSetPasswordForm,
    LinkSubmissionForm,
    SimpleSearchForm,
)
from .theme import styles

from curriculum_tracking.constants import (
    COMPETENT,
    EXCELLENT,
)

User = get_user_model()

board_columns = [
    {
        "title": "Backlog",
        "id": f"{AgileCard.READY}{AgileCard.BLOCKED}",
        "query": lambda user: AgileCard.objects.filter(
            Q(status=AgileCard.READY) | Q(status=AgileCard.BLOCKED)
        )
        .order_by("order")
        .filter(assignees=user),
    },
    {
        "title": "In Progress",
        "id": AgileCard.IN_PROGRESS,
        "query": lambda user: AgileCard.objects.filter(status=AgileCard.IN_PROGRESS)
        .order_by("order")
        .filter(Q(assignees=user) | Q(reviewers__in=(user,)))
        .distinct(),
    },
    {
        "title": "Review Feedback",
        "id": AgileCard.REVIEW_FEEDBACK,
        "query": lambda user: AgileCard.objects.filter(status=AgileCard.REVIEW_FEEDBACK)
        .order_by("order")
        .filter(Q(assignees=user) | Q(reviewers__in=(user,)))
        .distinct(),
    },
    {
        "title": "Review",
        "id": AgileCard.IN_REVIEW,
        "query": lambda user: AgileCard.objects.filter(status=AgileCard.IN_REVIEW)
        .order_by("order")
        .filter(Q(assignees=user) | Q(reviewers__in=(user,)))
        .distinct(),
    },
    {
        "title": "Complete",
        "id": AgileCard.COMPLETE,
        "query": lambda user: AgileCard.objects.filter(status=AgileCard.COMPLETE)
        .order_by("-order")
        .filter(assignees=user),
    },
]


def is_super(user):
    return user.is_superuser


def is_staff(user):
    return user.is_staff


def user_passes_test_or_forbidden(test_func):
    """
    Decorator for views that checks that the user passes the given test,
    returning a 403 Forbidden response if necessary. The default user_passes_test
    decorator redirects to the login page, which is not what we want for the
    frontend, or at least some of the frontend views.
    """

    def decorator(view_func):
        @login_required()
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden(
                render(request, "frontend/auth/page_permission_denied.html")
            )

        return _wrapped_view

    return decorator


def check_no_outstanding_reviews_on_card_action(view_func):
    """
    Decorator for action views that checks that the user has
    no outstanding card or pull request reviews.

    Decorated view must have card_id in kwargs.
    """

    def _wrapped_view(request, *args, **kwargs):
        assert "card_id" in kwargs
        card = get_object_or_404(AgileCard, pk=kwargs["card_id"])

        if helpers.agile_card_reviews_outstanding(request.user):
            return render(
                request,
                "frontend/user/board/js_exec_action_show_card_alert.html",
                {"card": card, "alert_message": "You have outstanding card reviews"},
            )

        if helpers.pull_request_reviews_outstanding(request.user):
            return render(
                request,
                "frontend/user/board/js_exec_action_show_card_alert.html",
                {
                    "card": card,
                    "alert_message": "You have outstanding pull request reviews.",
                },
            )

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def can_view_user_board(logged_in_user):
    request = get_current_request()
    viewed_user_id = request.resolver_match.kwargs.get("user_id")

    if logged_in_user.id == viewed_user_id or logged_in_user.is_superuser:
        return True

    viewed_user_obj = get_object_or_404(User, pk=viewed_user_id)
    viewed_user_teams = viewed_user_obj.teams()

    if len(viewed_user_teams):
        checker = ObjectPermissionChecker(logged_in_user)
        checker.prefetch_perms(viewed_user_teams)
        for view_permission in Team.PERMISSION_VIEW:
            if any(
                (checker.has_perm(view_permission, team) for team in viewed_user_teams)
            ):
                return True

    return False


def can_view_team(logged_in_user):
    request = get_current_request()
    viewed_team_id = request.resolver_match.kwargs.get("team_id")

    if logged_in_user.is_superuser:
        return True

    viewed_team_obj = get_object_or_404(Team, pk=viewed_team_id)
    checker = ObjectPermissionChecker(logged_in_user)

    for view_permission in Team.PERMISSION_VIEW:
        if checker.has_perm(
            view_permission,
            viewed_team_obj,
        ):
            return True

    return False


def user_login(request):
    form = CustomAuthenticationForm(request=request)
    context = {"form": form}

    if request.method == "POST":
        form = CustomAuthenticationForm(request=request, data=request.POST)
        context = {"form": form}

        if form.is_valid():
            login(
                request=request,
                user=form.user_cache,
            )

            redirect_to = request.GET.get(
                "next",
                reverse_lazy("user_board", kwargs={"user_id": form.user_cache.id}),
            )

            return redirect(redirect_to)

    return render(
        request,
        "frontend/auth/page_login.html",
        context,
    )


@login_required()
def user_logout(request):
    logout(request)
    return redirect(reverse_lazy("user_login"))


def _send_password_reset_email(request, form: ForgotPasswordForm) -> None:
    current_site = get_current_site(request)
    subject = "Reset your Password"

    body = render_to_string(
        template_name="frontend/auth/email_password_reset.html",
        context={
            "domain": current_site.domain,
            "url": form.get_password_reset_url(),
        },
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=strip_tags(body),
        from_email=None,
        to=[form.cleaned_data["email"]],
    )
    email.attach_alternative(body, "text/html")
    email.send(fail_silently=False)


def user_forgot_password(request):
    form = ForgotPasswordForm()
    context = {"form": form}

    if request.method == "POST":
        form = ForgotPasswordForm(data=request.POST)
        context.update({"form": form})

        if form.is_valid():
            if form.user_exists():
                _send_password_reset_email(request, form)
            return redirect(reverse_lazy("user_password_reset_done"))

    return render(request, "frontend/auth/page_forgot_password.html", context)


def user_password_reset_done(request):
    return render(request, "frontend/auth/page_password_reset_done.html")


def user_reset_password(request, token):
    signer = ForgotPasswordForm.signer
    try:
        email = signer.unsign(token, max_age=60 * 10)
    except (SignatureExpired, BadSignature):
        return render(
            request,
            "frontend/auth/page_password_reset.html",
            {"error": "Invalid token or expired token. Please try resetting again."},
        )

    user = User.objects.get(email=email)
    form = CustomSetPasswordForm(user=user)

    context = {"form": form}

    if request.method == "POST":
        form = CustomSetPasswordForm(user=user, data=request.POST)
        context.update({"form": form})

        if form.is_valid():
            form.save()
            messages.add_message(
                request=request,
                level=messages.INFO,
                message="Password reset successfully. You can now login.",
                extra_tags=styles["alert_info"],
            )
            return redirect(reverse_lazy("user_login"))

    return render(request, "frontend/auth/page_password_reset.html", context)


@user_passes_test_or_forbidden(can_view_user_board)
def user_board(request, user_id):
    """The user board page. this displays the kanban board for a user"""
    user = get_object_or_404(User, id=user_id)
    context = {"user": user, "columns": board_columns}
    return render(request, "frontend/user/board/page.html", context)


@user_passes_test_or_forbidden(can_view_user_board)
def view_partial_user_board_column(request, user_id, column_id):
    """The contents of one of the columns of the user's board"""
    current_card_count = int(request.GET.get("count", 0))
    limit = 10

    user = get_object_or_404(User, id=user_id)
    all_cards = [d for d in board_columns if d["id"] == column_id][0]["query"](user)

    cards = all_cards[current_card_count : current_card_count + limit]
    has_next_page = len(all_cards) > current_card_count + limit

    context = {
        "cards": cards,
        "user_id": user_id,
        "column_id": column_id,
        "has_next_page": has_next_page,
    }
    return render(
        request, "frontend/user/board/view_partial_user_board_column.html", context
    )


def check_user_can_start_card(logged_in_user):
    request = get_current_request()
    card_id = request.resolver_match.kwargs.get("card_id")

    card = get_object_or_404(AgileCard, pk=card_id)
    return card.request_user_can_start(logged_in_user)


@csrf_exempt
@user_passes_test_or_forbidden(check_user_can_start_card)
@check_no_outstanding_reviews_on_card_action
def action_start_card(request, card_id):
    """The card is in the backlog and the user has chosen to start it"""
    card = get_object_or_404(AgileCard, id=card_id)

    content_item_type = card.content_item.content_type

    if content_item_type == ContentItem.TOPIC:
        card.start_topic()
    elif content_item_type == ContentItem.PROJECT:
        card.start_project()
    else:
        raise NotImplemented(
            f"Cannot start card of type {card.content_item.content_type}"
        )

    log_creators.log_card_started(card=card, actor_user=request.user)

    return render(
        request,
        "frontend/user/board/js_exec_action_card_moved.html",
        {
            "card": card,
        },
    )


@user_passes_test_or_forbidden(can_view_user_board)
def progress_details(
    request,
    content_type,
    id,
):
    if content_type == "topic":
        course_component = get_object_or_404(TopicProgress, id=id)

    if content_type == "project":
        course_component = get_object_or_404(RecruitProject, id=id)

    form = None

    timeline = []
    log_entries = LogEntry.objects.filter(
        object_1_content_type=ContentType.objects.get_for_model(course_component),
        object_1_id=course_component.id,
    ).prefetch_related("event_type")

    for entry in log_entries:
        timeline.append(
            {
                "timestamp": entry.timestamp,
                "event_type": entry.event_type.name,
                "actor": entry.actor_user,
            }
        )

    if content_type == "project":
        reviews = RecruitProjectReview.objects.filter(recruit_project=course_component)
        for review in reviews:
            timeline.append(
                {
                    "timestamp": review.timestamp,
                    "event_type": f"REVIEW {review.status_nice} validated={review.validated_nice} trusted={review.trusted}",
                    "actor": review.reviewer_user,
                }
            )

    if content_type == "project" and course_component.submission_type_nice == "link":
        form = LinkSubmissionForm()

        if request.method == "POST":
            form = LinkSubmissionForm(request.POST)

            if form.is_valid():
                link_submission = form.cleaned_data["link_submission"]

                if course_component.link_submission_is_valid(link_submission):
                    course_component.link_submission = link_submission
                    course_component.save()

                else:
                    form.add_error(
                        "submission_link",
                        course_component.link_submission_invalid_message(
                            link_submission
                        ),
                    )

    board_status = [
        value
        for key, value in AgileCard.STATUS_CHOICES
        if key == course_component.agile_card.status
    ][0]

    context = {
        "course_component": course_component,
        "board_status": board_status,
        "link_submission_form": form,
        "timeline": sorted(timeline, key=lambda d: d["timestamp"]),
    }

    return render(
        request,
        "frontend/progress_details/page.html",
        context,
    )


def check_user_can_request_review_on_card(logged_in_user):
    request = get_current_request()
    card_id = request.resolver_match.kwargs.get("card_id")

    card: AgileCard = get_object_or_404(AgileCard, pk=card_id)
    return card.request_user_can_request_review(user=logged_in_user)


@csrf_exempt
@user_passes_test_or_forbidden(check_user_can_request_review_on_card)
@check_no_outstanding_reviews_on_card_action
def action_request_review(request, card_id):
    """The card is in progress or review feedback and the user has chosen to request review"""
    card = get_object_or_404(AgileCard, id=card_id)

    if card.recruit_project:
        card.recruit_project.request_review(force_timestamp=timezone.now())
    else:
        raise NotImplementedError("Only project cards can request review")

    log_creators.log_card_review_requested(card=card, actor_user=request.user)

    card.refresh_from_db()

    assert (
        card.status == AgileCard.IN_REVIEW
    ), f"Expected to be in review, but got {card.status}"

    return render(
        request,
        "frontend/user/board/js_exec_action_card_moved.html",
        {
            "card": card,
        },
    )


def check_user_can_cancel_review_request_on_card(logged_in_user):
    request = get_current_request()
    card_id = request.resolver_match.kwargs.get("card_id")

    card: AgileCard = get_object_or_404(AgileCard, pk=card_id)
    return card.request_user_can_cancel_review_request(user=logged_in_user)


@csrf_exempt
@user_passes_test_or_forbidden(check_user_can_cancel_review_request_on_card)
def action_cancel_review_request(request, card_id):
    """The card is in review and the user has chosen to cancel the review request"""
    card = get_object_or_404(AgileCard, id=card_id)

    if card.recruit_project:
        card.recruit_project.cancel_request_review()
    else:
        raise NotImplementedError("Only project cards can cancel review request")

    log_creators.log_card_review_request_cancelled(card=card, actor_user=request.user)

    card.refresh_from_db()

    assert (
        card.status == AgileCard.IN_PROGRESS
    ), f"Expected to be in progress, but got {card.status}"

    return render(
        request,
        "frontend/user/board/js_exec_action_card_moved.html",
        {
            "card": card,
        },
    )


def check_user_can_finish_topic(logged_in_user):
    request = get_current_request()
    card_id = request.resolver_match.kwargs.get("card_id")

    card: AgileCard = get_object_or_404(AgileCard, pk=card_id)
    card_assignees = card.assignees.all()

    if logged_in_user in card_assignees:
        return True

    card_teams = card.get_teams()
    checker = ObjectPermissionChecker(logged_in_user)
    checker.prefetch_perms(card_teams)

    return card.request_user_can_finish_topic(logged_in_user)


@csrf_exempt
@user_passes_test_or_forbidden(check_user_can_finish_topic)
@check_no_outstanding_reviews_on_card_action
def action_finish_topic(request, card_id):
    """The card is in progress and the user has chosen to finish it"""
    card: AgileCard = get_object_or_404(AgileCard, id=card_id)

    if card.topic_progress:
        card.finish_topic()
    else:
        raise NotImplementedError("Only topic cards can be finished.")

    log_creators.log_card_moved_to_complete(
        card=card,
        actor_user=request.user,
    )

    card.refresh_from_db()

    assert (
        card.status == AgileCard.COMPLETE
    ), f"Expected to be completed, but got {card.status}"

    return render(
        request,
        "frontend/user/board/js_exec_action_card_moved.html",
        {
            "card": card,
        },
    )


def check_user_can_stop_card(logged_in_user):
    request = get_current_request()
    card_id = request.resolver_match.kwargs.get("card_id")

    card: AgileCard = get_object_or_404(AgileCard, pk=card_id)
    return card.request_user_can_stop_card(user=logged_in_user)


@csrf_exempt
@user_passes_test_or_forbidden(check_user_can_stop_card)
def action_stop_card(request, card_id):
    """The card is in in-progress and the user wants to stop it"""
    card = get_object_or_404(AgileCard, id=card_id)

    content_type = card.content_item.content_type

    if content_type == ContentItem.TOPIC:
        card.stop_topic()
    elif content_type == ContentItem.PROJECT:
        card.stop_project()
    else:
        raise NotImplementedError("Only topics and projects can be stopped")

    log_creators.log_card_stopped(card=card, actor_user=request.user)

    card.refresh_from_db()

    assert (
        card.status == AgileCard.READY
    ), f"Expected to be in backlog, but got {card.status}"

    return render(
        request,
        "frontend/user/board/js_exec_action_card_moved.html",
        {
            "card": card,
        },
    )


@login_required()
def view_partial_users_list(request):
    user = request.user

    all_users = User.objects.filter(active=True)
    total_user_count = all_users.count()

    if user.is_superuser:
        filtered_users = all_users
    else:
        permitted_teams = user.get_permissioned_teams(perms=tuple(Team.PERMISSION_VIEW))
        permitted_users = []
        for team in permitted_teams:
            permitted_users.extend(team.active_users.all())

        permitted_user_ids = [user.id for user in permitted_users]

        # Convert the list of user IDs back to a QuerySet for ease of filtering
        filtered_users = User.objects.filter(id__in=permitted_user_ids, active=True)

    if request.method == "POST":
        form = SimpleSearchForm(request.POST)

        if form.is_valid():
            search_term = form.cleaned_data["search_term"]

            filtered_users = User.get_users_from_search_term(
                search_term, filtered_users
            )

    limit = 20
    current_user_count = int(request.GET.get("count", 0))
    users = filtered_users[current_user_count : current_user_count + limit]
    has_next_page = total_user_count > current_user_count + limit

    context = {
        "users": users,
        "has_next_page": has_next_page,
    }

    return render(
        request,
        "frontend/users_and_teams_nav/view_partial_users_list.html",
        context,
    )


@login_required()
def users_and_teams_nav(request):
    """This lets a user search for users and teams. It should only display what the logged in user is allowed to see"""
    # teams = Team.objects.order_by("name")
    # users = User.objects.order_by("email")
    context = {
        # "teams": teams,
        # "users": users,
    }
    return render(request, "frontend/users_and_teams_nav/page.html", context)


@login_required()
def view_partial_teams_list(request):
    user = request.user

    from guardian.shortcuts import get_objects_for_user

    all_teams = Team.objects.filter(active=True).order_by("name")
    total_teams_count = all_teams.count()

    if user.is_superuser:
        teams = all_teams
    else:
        teams = get_objects_for_user(
            user=user, perms=Team.PERMISSION_VIEW, klass=all_teams, any_perm=True
        )

    limit = 20
    current_team_count = int(request.GET.get("count", 0))
    teams = teams[current_team_count : current_team_count + limit]
    has_next_page = total_teams_count > current_team_count + limit

    context = {
        "teams": teams,
        "has_next_page": has_next_page,
    }

    return render(
        request,
        "frontend/users_and_teams_nav/view_partial_teams_list.html",
        context,
    )


@user_passes_test_or_forbidden(can_view_team)
def view_partial_team_users_list(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    users = team.active_users.order_by("email")
    context = {
        "users": users,
    }
    return render(
        request,
        "frontend/users_and_teams_nav/view_partial_team_users_list.html",
        context,
    )


@user_passes_test_or_forbidden(can_view_team)
def team_dashboard(request, team_id):
    """The team dashboard page. this displays the kanban board for a team"""
    team = get_object_or_404(Team, id=team_id)
    context = {
        "team": team,
    }
    return render(request, "frontend/team/dashboard/page.html", context)


@user_passes_test_or_forbidden(can_view_user_board)
def view_partial_team_user_progress_chart(request, user_id):
    user = get_object_or_404(User, id=user_id)

    skill_tags = Tag.objects.filter(name__startswith="skill/")
    skill_names = []
    skill_values = []

    for skill in skill_tags:
        cards = AgileCard.objects.filter(
            content_item__tags=skill,
            assignees=user,
            content_item__content_type=ContentItem.PROJECT,
        ).prefetch_related("recruit_project")

        skill_total = cards.count()
        complete_count = cards.filter(status=AgileCard.COMPLETE).count()

        if skill_total == 0:
            continue

        skill_names.append(skill.name.replace("skill/", ""))

        final = int(complete_count / skill_total * 100)
        skill_values.append(final)

    context = {
        "canvas_id": f"progress-chart-{ user.id }",
        "chart_args": json.dumps(
            {
                "type": "polarArea",
                "options": {
                    "scale": {"r": {"min": 0, "max": 100}},
                    "plugins": {
                        "legend": {"position": "right"},
                    },
                },
                "data": {
                    "labels": skill_names,
                    "datasets": [
                        {
                            "data": skill_values,
                        },
                    ],
                },
            },
            indent=2,
        ),
    }

    return render(request, "frontend/js_exec_render_chartjs.html", context)


## Project review coordination


@user_passes_test(is_staff)
def project_review_coordination_unclaimed(request):
    from project_review_coordination.models import ProjectReviewBundleClaim

    ProjectReviewBundleClaim.objects.filter(is_active=True).filter(
        due_timestamp__lt=timezone.now()
    ).update(
        is_active=False
    )  # TODO: This should be in a cron job or dramatiq task

    cards = ProjectReviewBundleClaim.get_projects_user_can_review(request.user)

    bundles = {}
    for card in cards:

        project = card.recruit_project
        staff_positive_reviews_since_request = (
            project.project_reviews.filter(
                timestamp__gte=project.review_request_time
            ).filter(reviewer_user__is_staff=True)
        ).count()
        # TODO: Make this faster by using an annotation on the initial query
        # it was a bit of a pain to attempt because the django docs site was down :/

        is_trusted = card.request_user_is_trusted()

        if staff_positive_reviews_since_request >= 2 and not is_trusted:
            # if too many staff have seen this already, no need for another
            continue

        flavours = sorted(card.recruit_project.flavour_names)
        content_item_id = card.content_item.id
        bundle_id = f"{content_item_id}.{flavours}"

        if bundle_id not in bundles:
            bundles[bundle_id] = {
                "title": card.content_item.title,
                "flavours": flavours,
                "oldest_review_request_time": card.recruit_project.review_request_time,
                "project_ids": [],
                "card_count": 0,
                "is_trusted": is_trusted,
            }

        bundles[bundle_id]["card_count"] += 1
        bundles[bundle_id]["project_ids"].append(card.recruit_project_id)

    context = {
        "bundles": bundles.values(),
    }

    return render(
        request,
        "frontend/project_review_coordination/unclaimed/page.html",
        context=context,
    )


@user_passes_test(is_staff)
def project_review_coordination_my_claims(request):
    from project_review_coordination.models import ProjectReviewBundleClaim

    claims = ProjectReviewBundleClaim.objects.filter(claimed_by_user=request.user)
    active_claims = claims.filter(is_active=True)

    context = {
        "active_claims": active_claims,
    }
    return render(
        request,
        "frontend/project_review_coordination/my_claims/page.html",
        context=context,
    )


@user_passes_test(is_staff)
def project_review_coordination_all_claims(request):
    from project_review_coordination.models import ProjectReviewBundleClaim

    claims = ProjectReviewBundleClaim.objects.filter()
    active_claims = claims.filter(is_active=True)

    context = {
        "active_claims": active_claims,
    }

    return render(
        request,
        "frontend/project_review_coordination/all_claims/page.html",
        context=context,
    )


@user_passes_test(is_staff)
def action_project_review_coordination_claim_bundle(request):
    from project_review_coordination.models import ProjectReviewBundleClaim
    from curriculum_tracking.models import RecruitProject

    user = request.user
    project_ids = request.POST.getlist("project_ids")
    assert len(project_ids) > 0, "No project_ids provided"
    projects = RecruitProject.objects.filter(id__in=project_ids).exclude(
        project_review_bundle_claims__is_active=True
    )

    # TODO: filter out projects that the current user has reviewed since the last review request time
    # TODO: filter out project that the current user doesn't have permission to review

    project_count = projects.count()
    if project_count > 0:
        claim = ProjectReviewBundleClaim.objects.create(claimed_by_user=user)
        claim.projects_to_review.set(projects)

        context = {
            "project_count": project_count,
        }
        return render(
            request,
            "frontend/project_review_coordination/unclaimed/view_partial_claim_success.html",
            context=context,
        )

    return render(
        request,
        "frontend/project_review_coordination/unclaimed/view_partial_claim_failed.html",
    )


@user_passes_test(is_staff)
def action_project_review_coordination_unclaim_bundle(request, claim_id):
    from project_review_coordination.models import ProjectReviewBundleClaim

    instance = get_object_or_404(ProjectReviewBundleClaim, id=claim_id)

    instance.is_active = False
    instance.save()

    return render(
        request,
        "frontend/project_review_coordination/view_partial_unclaim_bundle.html",
    )


@user_passes_test(is_staff)
def action_project_review_coordination_add_time(request, claim_id):
    from project_review_coordination.models import ProjectReviewBundleClaim

    instance = get_object_or_404(ProjectReviewBundleClaim, id=claim_id)

    instance.due_timestamp = instance.due_timestamp + timezone.timedelta(minutes=15)
    instance.save()

    return render(
        request,
        "frontend/project_review_coordination/view_partial_claim_due_timestamp.html",
        context={"claim": instance},
    )


# DASHBOARDING


@user_passes_test(is_staff)
def dashboard_project_review_health(request):
    """
    Display some stats about project reviews
    """

    DAYS = 7

    recently_closed_projects = RecruitProject.objects.filter(
        complete_time__gte=timezone.now() - timezone.timedelta(days=DAYS)
    )

    closing_reviews = {
        # email: {
        #   "user": User,
        #   "total": 0,
        #   "total wait time": 0,
        #  "closing reviews": [review1, review2]
        # max_wait_time: timedelta
        # min_wait_time: timedelta
        # }
    }

    for project in recently_closed_projects:
        recent_reviews = project.project_reviews.filter(
            timestamp__gte=project.review_request_time
        ).order_by("-timestamp")[:2]
        closing_reviewer = recent_reviews[0].reviewer_user
        if len(recent_reviews) < 2:
            continue
        delta = recent_reviews[0].timestamp - recent_reviews[1].timestamp
        closing_reviews[closing_reviewer.email] = closing_reviews.get(
            closing_reviewer.email,
            {
                "user": closing_reviewer,
                "total": 0,
                "total_wait_time": 0,
                "max_wait_time": delta,
                "min_wait_time": delta,
                "closing_reviews": [],
            },
        )
        closing_reviews[closing_reviewer.email]["total"] += 1
        closing_reviews[closing_reviewer.email][
            "total_wait_time"
        ] += delta.total_seconds()
        closing_reviews[closing_reviewer.email]["closing_reviews"].append(
            recent_reviews[0]
        )
        if delta > closing_reviews[closing_reviewer.email]["max_wait_time"]:
            closing_reviews[closing_reviewer.email]["max_wait_time"] = delta
        if delta < closing_reviews[closing_reviewer.email]["min_wait_time"]:
            closing_reviews[closing_reviewer.email]["min_wait_time"] = delta

    for email, data in closing_reviews.items():
        data["average_wait_time"] = timezone.timedelta(
            seconds=data["total_wait_time"] / data["total"]
        )

    closing_reviews_sorted = sorted(closing_reviews.values(), key=lambda x: x["total"])

    # get number of competence reviews done in the last DAYS days per staff member

    all_staff_competence_reviews = RecruitProjectReview.objects.filter(
        timestamp__gte=timezone.now() - timezone.timedelta(days=DAYS)
    ).filter(reviewer_user__is_staff=True)

    competence_reviews = {}
    for review in all_staff_competence_reviews:
        competence_reviews[review.reviewer_user.email] = competence_reviews.get(
            review.reviewer_user.email,
            {
                "user": review.reviewer_user,
                "total": 0,
                "competent": 0,
                "not_yet_competent": 0,
                "excellent": 0,
                "red_flag": 0,
                "trusted": 0,
                "complete_review_cycle": 0,
                "bouncey_review_cycle": 0,
                "incorrect": 0,
                "correct": 0,
                "contradicted": 0,
                "not_yet_validated": 0,
            },
        )
        current = competence_reviews[review.reviewer_user.email]
        current["total"] += 1
        current[review.status_nice.replace(" ", "_")] += 1
        if review.trusted:
            current["trusted"] += 1
        if review.status in [COMPETENT, EXCELLENT]:
            current[review.validated_nice.replace(" ", "_")] += 1
        else:
            if review.complete_review_cycle == True:
                current["complete_review_cycle"] += 1
            elif review.complete_review_cycle == False:
                current["bouncey_review_cycle"] += 1

    competence_reviews_sorted = sorted(
        competence_reviews.values(), key=lambda d: d["total"]
    )

    longest_running_open_cards = (
        AgileCard.objects.filter(
            Q(status=AgileCard.IN_REVIEW)
            | Q(status=AgileCard.IN_PROGRESS)
            | Q(status=AgileCard.REVIEW_FEEDBACK)
        )
        .filter(content_item__content_type=ContentItem.PROJECT)
        .filter(assignees__active=True)
        .filter(assignees__is_staff=False)
        .exclude(assignees__groups__team__active=False)
        .order_by("recruit_project__start_time")
        .prefetch_related("recruit_project")
    )

    longest_running_open_projects = [
        card.recruit_project for card in longest_running_open_cards[:15]
    ]

    context = {
        "closing_reviews": closing_reviews_sorted,
        "competence_review_counts": competence_reviews_sorted,
        "longest_running_open_projects": longest_running_open_projects,
    }

    return render(
        request,
        "frontend/dashboards/project_review_health/page.html",
        context=context,
    )
