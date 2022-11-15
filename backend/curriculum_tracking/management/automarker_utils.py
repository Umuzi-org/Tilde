import requests
from pprint import pprint
from backend.settings import CURRICULUM_TRACKING_REVIEW_BOT_EMAIL
from core.models import User
from curriculum_tracking.models import AgileCard, RecruitProjectReview
from curriculum_tracking.constants import NOT_YET_COMPETENT, COMPETENT
from django.utils import timezone
from pprint import pprint


def _get_bot_user():
    bot_user, _ = User.objects.get_or_create(email=CURRICULUM_TRACKING_REVIEW_BOT_EMAIL)
    return bot_user


def _get_automark_result(repo_url, content_item_id, flavours):

    url = "http://localhost:1337/mark-project"  # TODO. use configuration
    headers = {"Content-Type": "application/json"}
    json = {
        "repoUrl": repo_url,
        "contentItemId": content_item_id,
        "flavours": flavours,
    }
    pprint(json)
    response = requests.post(
        url,
        headers=headers,
        json=json,
    )
    return response.json()


def confirm_continue(message):
    answer = ""
    while answer not in ["Y", "N"]:
        print(f"message = \n```\n{message}\n```")
        answer = input("\n\nWould you like to continue? Y/N").upper()
    return answer == "Y"


def add_review(card, status, comments):
    base_comments = (
        "Hello! I'm a robot 🤖\n\nI'm here to give you quick feedback about your code."
    )
    if status == COMPETENT:
        full_comments = f"{base_comments} {comments}." if comments else base_comments
        full_comments = f"{full_comments} Keep up the good work :)"
    else:
        full_comments = f"{base_comments} Something went wrong when I marked your code. Most people don't get things right on the first try, just keep trying, I'm sure you'll figure it out! \n\nHere are some details:\n\n{comments}\n\nIf the feedback doesn't make sense please reach out to one of the humans that work here and they'll be happy to help you understand. Humans are great like that"
    RecruitProjectReview.objects.create(
        status=status,
        timestamp=timezone.now(),
        comments=full_comments,
        recruit_project=card.recruit_project,
        reviewer_user=_get_bot_user(),
    )


def get_cards_needing_review(content_item, flavours=None):
    cards = (
        AgileCard.objects.filter(status=AgileCard.IN_REVIEW)
        .filter(content_item=content_item)
        .filter(assignees__active__in=[True])
    )
    for card in cards:
        if flavours and not card.flavours_match(flavours):
            continue

        print(f"{card.assignees.first()} - {card.title} {card.flavour_names}")

        has_review = (
            card.recruit_project.project_reviews.filter(
                timestamp__gt=card.recruit_project.review_request_time
            )
            .filter(reviewer_user=_get_bot_user())
            .count()
        )

        if has_review:
            print("... already has a review")
            continue

        yield card


def automark_card(card, debug_mode):
    result = _get_automark_result(
        repo_url=card.recruit_project.repository.ssh_url,
        content_item_id=card.content_item_id,
        flavours=card.flavour_names,
    )
    pprint(result)
    if result["status"] == "OK":

        add_review(card=card, status=COMPETENT, comments="All our checks passed")
    elif result["status"] == "FAIL":

        # step_name = result['actionName']
        result = result["result"]

        comments = f"*{result['message']}*"
        if errors := result.get("errors"):
            errors = "\n".join([f"- {s}" for s in errors])
            comments = f"{comments}\n{errors}"

        if debug_mode:
            # print(f"comments:\n\n{comments}")
            message = f"You are about to leave a negative review:\n\n"
            message += f"Repo url: {card.recruit_project.repository.ssh_url}\n"
            message += f"Card url: https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/card/{card.id}\n"
            message += f"review comments:\n\n{comments}"

            if confirm_continue(message):
                add_review(
                    card=card,
                    status=NOT_YET_COMPETENT,
                    comments=comments,
                )
        else:

            add_review(
                card=card,
                status=NOT_YET_COMPETENT,
                comments=comments,
            )
    else:

        pprint(result)
