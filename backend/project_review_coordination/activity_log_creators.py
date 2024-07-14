from activity_log.models import LogEntry, EventType


BUNDLE_CLAIMED = "BUNDLE_CLAIMED"
BUNDLE_UNCLAIMED = "BUNDLE_UNCLAIMED"
TIME_ADDED = "BUNDLE_TIME_ADDED"
BUNDLE_EXPIRED = "BUNDLE_EXPIRED"
BUNDLE_COMPLETED = "BUNDLE_COMPLETED"


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
