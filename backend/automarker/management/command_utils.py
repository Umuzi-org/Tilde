from pprint import pprint

from curriculum_tracking.models import AgileCard
from curriculum_tracking.constants import NOT_YET_COMPETENT, COMPETENT
from backend.settings import AUTO_MARKER_CONFIGURATION_PATH

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from automarker.utils import (
    get_bot_user,
    get_automark_result,
    add_review,
    get_fail_review_comments,
    STATUS_OK,
    STATUS_FAIL,
)


def confirm_continue(message):
    answer = ""
    while answer not in ["Y", "N"]:
        print(f"message = \n```\n{message}\n```")
        answer = input("\n\nWould you like to continue? Y/N").upper()
    return answer == "Y"


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
            .filter(reviewer_user=get_bot_user())
            .count()
        )

        if has_review:
            print("... already has a review")
            continue

        yield card


def automark_project(project, debug_mode):
    result = get_automark_result(
        link_submission=project.link_submission,
        repo_url=project.repository.ssh_url if project.repository else None,
        content_item_id=project.content_item_id,
        flavours=project.flavour_names,
    )
    pprint(result)
    if result["status"] == STATUS_OK:

        add_review(project=project, api_result=result)
    elif result["status"] == STATUS_FAIL:

        # step_name = result['actionName']
        # result = result["result"]
        print("============")
        print(result)
        print("============")

        if debug_mode:
            message = f"You are about to leave a negative review:\n\n"
            if project.repository:
                message += f"Repo url: {project.repository.ssh_url}\n"
            message += f"Link url: {project.link_submission}\n"
            try:
                card = project.agile_card
                message += f"Card url: https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/card/{card.id}\n"
            except AgileCard.DoesNotExist:
                pass

            comments = get_fail_review_comments(result)
            message += f"review comments:\n\n{comments}"

            if confirm_continue(message):
                add_review(project=project, api_result=result)
        else:

            add_review(project=project, api_result=result)

    else:
        pprint(result)
        raise Exception(f"result['status'] = {result['status']}")


def get_config_from_file():
    with open(AUTO_MARKER_CONFIGURATION_PATH, "r") as f:
        return yaml.load(f, Loader)
