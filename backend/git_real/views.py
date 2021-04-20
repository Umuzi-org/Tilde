from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from git_real.models import PullRequest
from backend.settings import GIT_REAL_WEBHOOK_SECRET
from core.permissions import RequestMethodIs
from .permissions import IsWebhookSignatureOk


@api_view(["POST", "GET"])
@permission_classes([RequestMethodIs("GET") | IsWebhookSignatureOk])
def github_webhook(request):
    """this is where requests grom Github arrives.
    based on https://docs.github.com/en/developers/webhooks-and-events/creating-webhooks"""
    assert (
        GIT_REAL_WEBHOOK_SECRET
    ), f"GIT_REAL_WEBHOOK_SECRET environmental variable is not set"
    if request.method == "POST":

        event = request.headers.get("X-Github-Event") or request.data.get(
            "headers", {}
        ).get("X-Github-Event")
        assert event, f"no event listed. headers = {request.headers}"
        if event == "pull_request":
            request.data["repository"]["full_name"]

            PullRequest.create_or_update_from_github_api_data(
                repo_full_name=request.data["repository"]["full_name"],
                pull_request_data=request.data["pull_request"],
                repo_missing_ok=True,
            )
        # elif event == "pull_request_review":
        #     todo
        # elif event == "pull_request_review_comment":
        #     todo
        # elif event == "push":
        #     todo
        # else:
        #     raise Exception(f"unhandled event type: {event}")

        return Response({})

    return Response({"status": "This endpoint exists"})


# def index(request):
#     if request.method == "POST":
#         form = TeamForm(request.POST)
#         if form.is_valid():
#             cohort_id = form.cleaned_data["cohort"]
#             product_team_id = form.cleaned_data["product_team"]
#             staff = form.cleaned_data["staff"]
#             everyone = form.cleaned_data.get("everyone")

#             if cohort_id:
#                 url = reverse("cohort_commits", kwargs={"id": cohort_id})
#             if product_team_id:
#                 url = reverse("product_commits", kwargs={"id": product_team_id})
#             if staff:
#                 url = reverse("staff_commits")
#             if everyone:
#                 url = reverse("all_commits")

#             return HttpResponseRedirect(url)
#     else:
#         form = TeamForm()
#     return render(request, "git_real/select_team.html", {"form": form})


# def commit_history_graph(request, id=None):
#     import plotly.graph_objects as go
#     import plotly.express as px
#     import pandas as pd

#     url_name = resolve(request.path_info).url_name

#     days_past = 14

#     cutoff = timezone.now() - datetime.timedelta(days=days_past)
#     if url_name == "cohort_commits":
#         cohort = Cohort.objects.get(pk=id)
#         users = cohort.get_member_users()
#         heading = f"Commits for {cohort}"
#     elif url_name == "product_commits":
#         product_team = ProductTeam.objects.get(pk=id)
#         users = product_team.get_member_users()
#         heading = f"Commits for product: {product_team}"

#     elif url_name == "staff_commits":
#         users = User.objects.filter(is_staff=True)
#         heading = "Commits for staff"
#     elif url_name == "all_commits":
#         users = User.objects.all()
#         heading = "All known commits"
#     else:
#         raise Exception(f"Unhandled option: {url_name}")
#     users = list(users)

#     all_commits = []

#     for user in users:
#         # TODO: this query is very inefficient and slow. Make it faster

#         commits = Commit.objects.filter(user=user, datetime__gte=cutoff)
#         all_commits.extend(commits)

#     # user_counts.sort(key=lambda t: t[0])
#     # user_positions =user_count

#     # df = px.data.iris() # iris is a pandas DataFrame

#     # all_commits = Commit.objects.filter(datetime__gte=cutoff)
#     # all_commits = Commit.objects.all()

#     user_emails = sorted([o.email for o in users])

#     df = pd.DataFrame(
#         [
#             [
#                 user_emails.index(commit.user.email),
#                 commit.commit_hash,
#                 commit.author_github_name,
#                 commit.author_email,
#                 commit.message,
#                 commit.branch,
#                 commit.datetime,
#                 commit.user.email,
#                 commit.user.id,
#                 commit.repository.full_name,
#                 str(commit.user.cohort or ""),
#                 ",".join([str(o) for o in commit.user.product_teams.all()]),
#                 commit.user.is_staff,
#             ]
#             for commit in all_commits
#             if commit.user
#         ],
#         columns=[
#             "index",
#             "commit_hash",
#             "commit.author_github_name",
#             "commit.author_email",
#             "message",
#             "branch",
#             "datetime",
#             "user.email",
#             "user.id",
#             "repository.full_name",
#             "cohort",
#             "products",
#             "is_staff",
#         ],
#     )

#     figure = px.scatter(df, x="datetime", y="index", hover_data=df.columns, height=800)

#     tomorrow = timezone.now().date() + datetime.timedelta(days=1)
#     all_dates = [
#         tomorrow - datetime.timedelta(days=days_past + 1 - i)
#         for i in range(days_past + 1)
#     ]

#     figure.update_layout(
#         yaxis={
#             "tickmode": "array",
#             "tickvals": list(range(len(users))),
#             "ticktext": user_emails,
#         },
#         xaxis={
#             "tickmode": "array",
#             "tickvals": all_dates,
#             # "tickvals": all_dates,
#             "showticklabels": True,
#             # "dtick": 60 * 60 * 24,
#             # "tick0": all_dates[0]
#             # "autotick": False,
#             # "type": "category",
#         },
#     ),
#     return render(
#         request,
#         "git_real/commits_log.html",
#         {"figure": figure.to_html(), "heading": heading},
#     )
