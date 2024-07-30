from activity_log.models import LogEntry, EventType


BUNDLE_CLAIMED = "PROJECT_REVIEW_BUNDLE_CLAIMED"
BUNDLE_UNCLAIMED = "PROJECT_REVIEW_BUNDLE_UNCLAIMED"
TIME_ADDED = "PROJECT_REVIEW_BUNDLE_TIME_ADDED"
BUNDLE_EXPIRED = "PROJECT_REVIEW_BUNDLE_EXPIRED"
BUNDLE_COMPLETED = "PROJECT_REVIEW_BUNDLE_COMPLETED"


def log_bundle_claimed(claim):
    event_type, _ = EventType.objects.get_or_create(name=BUNDLE_CLAIMED)
    LogEntry.objects.create(
        actor_user=claim.claimed_by_user,
        effected_user=claim.claimed_by_user,
        object_1=claim,
        event_type=event_type,
    )


def log_bundle_unclaimed(claim):
    event_type, _ = EventType.objects.get_or_create(name=BUNDLE_UNCLAIMED)
    LogEntry.objects.create(
        actor_user=claim.claimed_by_user,
        effected_user=claim.claimed_by_user,
        object_1=claim,
        event_type=event_type,
    )


def log_bundle_time_added(claim):
    event_type, _ = EventType.objects.get_or_create(name=TIME_ADDED)
    LogEntry.objects.create(
        actor_user=claim.claimed_by_user,
        effected_user=claim.claimed_by_user,
        object_1=claim,
        event_type=event_type,
    )


def log_bundle_expired(claim):
    event_type, _ = EventType.objects.get_or_create(name=BUNDLE_EXPIRED)
    LogEntry.objects.create(
        actor_user=None,
        effected_user=claim.claimed_by_user,
        object_1=claim,
        event_type=event_type,
    )


def log_bundle_completed(claim):
    event_type, _ = EventType.objects.get_or_create(name=BUNDLE_COMPLETED)
    LogEntry.objects.create(
        actor_user=claim.claimed_by_user,
        effected_user=claim.claimed_by_user,
        object_1=claim,
        event_type=event_type,
    )
