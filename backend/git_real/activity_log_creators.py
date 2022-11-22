from django.utils import timezone
from activity_log.models import LogEntry, EventType
from django.contrib.contenttypes.models import ContentType
import curriculum_tracking 


PR_MERGED = "PR_MERGED"
PR_CLOSED = "PR_CLOSED"
PR_OPENED = "PR_OPENED"
PR_REVIEWED = "PR_REVIEWED"
GIT_PUSH = "GIT_PUSH"


def log_pr_merged(pull_request):
    event_type, _ = EventType.objects.get_or_create(name=PR_MERGED)
    LogEntry.objects.get_or_create(
        actor_user=None,  # we don't care who clicked the merge button. Maybe we'll fill this in later
        effected_user=pull_request.user,
        object_1=pull_request,
        event_type=event_type,
    )


def log_pr_closed(pull_request):
    event_type, _ = EventType.objects.get_or_create(name=PR_CLOSED)

    match = LogEntry.objects.filter(
        actor_user=None,
        effected_user=pull_request.user,
        event_type=event_type,
        timestamp__gte=timezone.now() - timezone.timedelta(minutes=2),
        object_1_content_type = ContentType.objects.get_for_model(pull_request)
        ).filter(
            object_1_id = pull_request.id
        ).first()

    if match == None:
        LogEntry.objects.create(
            actor_user=None,  # we dont care who clicked the close button. Maybe we'll fill this in later
            effected_user=pull_request.user,
            object_1=pull_request,
            object_2= curriculum_tracking.models.RecruitProject.objects.filter(
                repository=pull_request.repository,
            ).order_by("pk").last(),
            event_type=event_type,
        )


def log_pr_opened(pull_request):

    event_type, _ = EventType.objects.get_or_create(name=PR_OPENED)

    match = LogEntry.objects.filter(
        actor_user=pull_request.user,
        effected_user=pull_request.user,
        object_1=pull_request,
        event_type=event_type,
        timestamp__gte=timezone.now() - timezone.timedelta(minutes=2),
    ).first()

    if match == None:
        LogEntry.objects.create(
            actor_user=pull_request.user,
            effected_user=pull_request.user,
            object_1=pull_request,
            event_type=event_type,
        )


def log_pr_reviewed(pull_request_review):
    event_type, _ = EventType.objects.get_or_create(name=PR_REVIEWED)

    repo = pull_request_review.pull_request.repository
    effected_project = repo.recruit_projects.first()

    effected_user = effected_project.recruit_users.first() if effected_project else None

    LogEntry.debounce_create(
        actor_user=pull_request_review.user,
        effected_user=repo.user or effected_user,
        object_1=pull_request_review,
        object_2=pull_request_review.pull_request.repository,
        event_type=event_type,
        timestamp=pull_request_review.submitted_at,
        debounce_seconds=False,
    )


def log_push_event(push):
    event_type, _ = EventType.objects.get_or_create(name=GIT_PUSH)
    
    repo = push.repository
    effected_project = repo.recruit_projects.first()

    effected_user = effected_project.recruit_users.first() if effected_project else None

    LogEntry.debounce_create(
        actor_user=repo.user,
        effected_user=repo.user or effected_user,
        object_1=push,
        object_2=push.repository,
        event_type=event_type,
        timestamp=push.pushed_at_time,
        debounce_seconds=False,
    )
