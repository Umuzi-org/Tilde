from activity_log.models import LogEntry, EventType


##################
# Card movements #
##################

CARD_STARTED = "CARD_STARTED"
CARD_STOPPED = "CARD_STOPPED"
CARD_REVIEW_REQUESTED = "CARD_REVIEW_REQUESTED"
CARD_REVIEW_REQUEST_CANCELLED = "CARD_REVIEW_REQUEST_CANCELLED"
CARD_MOVED_TO_COMPLETE = "CARD_MOVED_TO_COMPLETE"
CARD_MOVED_TO_REVIEW_FEEDBACK = "CARD_MOVED_TO_REVIEW_FEEDBACK"


def _log_card_movement(card, actor_user, event_type):
    for user in card.assignees.all():
        LogEntry.debounce_create(
            event_type=event_type,
            actor_user=actor_user,
            object_1=card.progress_instance,
            effected_user=user,
        )


def log_card_started(card, actor_user):
    event_type, _ = EventType.objects.get_or_create(name=CARD_STARTED)
    _log_card_movement(card, actor_user, event_type)


def log_card_stopped(card, actor_user):
    event_type, _ = EventType.objects.get_or_create(name=CARD_STOPPED)
    _log_card_movement(card, actor_user, event_type)


def log_card_review_requested(card, actor_user):
    event_type, _ = EventType.objects.get_or_create(name=CARD_REVIEW_REQUESTED)
    _log_card_movement(card, actor_user, event_type)


def log_card_review_request_cancelled(card, actor_user):
    event_type, _ = EventType.objects.get_or_create(name=CARD_REVIEW_REQUEST_CANCELLED)
    _log_card_movement(card, actor_user, event_type)


def log_card_moved_to_complete(card, actor_user):
    event_type, _ = EventType.objects.get_or_create(name=CARD_MOVED_TO_COMPLETE)
    _log_card_movement(card, actor_user, event_type)


def log_card_moved_to_review_feedback(card, actor_user):
    event_type, _ = EventType.objects.get_or_create(name=CARD_MOVED_TO_REVIEW_FEEDBACK)
    _log_card_movement(card, actor_user, event_type)


######################
# Competence reviews #
######################

COMPETENCE_REVIEW_DONE = "COMPETENCE_REVIEW_DONE"


def log_project_competence_review_done(review):
    event_type, _ = EventType.objects.get_or_create(name=COMPETENCE_REVIEW_DONE)
    for user in review.recruit_project.recruit_users.all():
        LogEntry.objects.get_or_create(
            actor_user=review.reviewer_user,
            effected_user=user,
            object_1=review,
            event_type=event_type,
        )


def log_topic_competence_review_done(review):
    event_type, _ = EventType.objects.get_or_create(name=COMPETENCE_REVIEW_DONE)
    LogEntry.objects.get_or_create(
        actor_user=review.reviewer_user,
        effected_user=review.topic_progress.user,
        object_1=review,
        event_type=event_type,
    )


######################
# Review agreements  #
######################
# COMPETENCE_REVIEW_INCORRECT = "COMPETENCE_REVIEW_INCORRECT"
# COMPETENCE_REVIEW_CORRECT = "COMPETENCE_REVIEW_CORRECT"
# COMPETENCE_REVIEW_CONTRADICTED = "COMPETENCE_REVIEW_CONTRADICTED"


# def log_competence_review_incorrect():
#     event_type, _ = EventType.objects.get_or_create(name=COMPETENCE_REVIEW_INCORRECT)
#     todo


# def log_competence_review_correct():
#     event_type, _ = EventType.objects.get_or_create(name=COMPETENCE_REVIEW_CORRECT)
#     todo


# def log_competence_review_contradicted():
#     event_type, _ = EventType.objects.get_or_create(name=COMPETENCE_REVIEW_CONTRADICTED)
#     todo


################
# Review Trust #
################

# REVIEW_TRUST_EARNED = "REVIEW_TRUST_EARNED"
# REVIEW_TRUST_REMOVED = "REVIEW_TRUST_REMOVED"

# def log_review_trust_created():
#     event_type, _ = EventType.objects.get_or_create(name=REVIEW_TRUST_EARNED)
#     todo


# def log_review_trust_removed():
#     event_type, _ = EventType.objects.get_or_create(name=REVIEW_TRUST_REMOVED)
#     todo
