from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from git_real.models import Repository, PullRequest, PullRequestReview

# from backend.settings import GIT_REAL_WEBHOOK_SECRET
from core.permissions import RequestMethodIs
from .permissions import IsWebhookSignatureOk


@api_view(["POST", "GET"])
@permission_classes([RequestMethodIs("GET") | IsWebhookSignatureOk])
def github_webhook(request):
    """this is where requests from Github arrives.
    based on https://docs.github.com/en/developers/webhooks-and-events/creating-webhooks"""

    if request.method == "POST":

        event = request.headers.get("X-Github-Event") or request.data.get(
            "headers", {}
        ).get("X-Github-Event")
        assert event, f"no event listed. headers = {request.headers}"

        if event in ["pull_request", "pull_request_review"]:
            repo_full_name = request.data["repository"]["full_name"]
            try:
                repo = Repository.objects.get(full_name=repo_full_name)
            except Repository.DoesNotExist:
                return

            pr = PullRequest.create_or_update_from_github_api_data(
                repo=repo,
                pull_request_data=request.data["pull_request"],
            )

            if event == "pull_request_review":

                PullRequestReview.create_or_update_from_github_api_data(
                    pull_request=pr, review_data=request.data["review"]
                )

        # elif event == "pull_request_review_comment":
        #     todo
        elif event == "push":
            todo
        # else:
        #     raise Exception(f"unhandled event type: {event}")

        return Response({})

    return Response({"status": "This endpoint exists"})
