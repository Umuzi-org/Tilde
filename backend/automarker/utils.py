from backend.settings import CURRICULUM_TRACKING_REVIEW_BOT_EMAIL
from core.models import User
from backend.settings import AUTOMARKER_SERVICE_BASE_URL
import requests
import urllib.parse
from curriculum_tracking.models import RecruitProjectReview
from django.utils import timezone
from curriculum_tracking.constants import COMPETENT, NOT_YET_COMPETENT
import json

STATUS_OK = "OK"
STATUS_FAIL = "FAIL"


def get_bot_user():
    bot_user, _ = User.objects.get_or_create(email=CURRICULUM_TRACKING_REVIEW_BOT_EMAIL)
    return bot_user


def get_automark_result(repo_url, link_submission, content_item_id, flavours):
    url = urllib.parse.urljoin(AUTOMARKER_SERVICE_BASE_URL, "mark-project")
    headers = {"Content-Type": "application/json"}
    json = {
        "repoUrl": repo_url or link_submission,
        "contentItemId": content_item_id,
        "flavours": flavours,
    }
    response = requests.post(
        url,
        headers=headers,
        json=json,
    )
    return response.json()


def get_fail_review_comments(api_result):
    errors = "\n".join([f"- {s}" for s in api_result["errors"]])
    return f"Something went wrong when I marked your code. Most people don't get things right on the first try, just keep trying, I'm sure you'll figure it out! \n\nHere are some details:\n\n*{api_result['message']}*{errors}"


def add_review(project, api_result):
    breakpoint()

    if api_result["status"] == STATUS_OK:
        status = COMPETENT
        comments = "Keep up the good work :)"
    elif api_result["status"] == STATUS_FAIL:
        status = NOT_YET_COMPETENT

        comments = get_fail_review_comments(api_result)
    else:
        raise Exception(json.dumps(api_result))

    base_comments = (
        "Hello! I'm a robot 🤖\n\nI'm here to give you quick feedback about your code."
    )
    RecruitProjectReview.objects.create(
        status=status,
        timestamp=timezone.now(),
        comments=f"{base_comments}\n\n{comments}",
        recruit_project=project,
        reviewer_user=get_bot_user(),
    )
