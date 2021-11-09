from django.utils import timezone
from activity_log.models import LogEntry, EventType


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
        object_1=pull_request,
        event_type=event_type,
        timestamp__gte=timezone.now() - timezone.timedelta(minutes=2),
    ).first()

    if match == None:
        LogEntry.objects.create(
            actor_user=None,  # we dont care who clicked the close button. Maybe we'll fill this in later
            effected_user=pull_request.user,
            object_1=pull_request,
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
    todo


def log_push_event():
    event_type, _ = EventType.objects.get_or_create(name=GIT_PUSH)
    todo
