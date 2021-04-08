import base64
from social_auth.github_api import Api
from git_real import models
from git_real.constants import GITHUB_DATETIME_FORMAT, GITHUB_DEFAULT_TIMEZONE
from timezone_helpers import timestamp_str_to_tz_aware_datetime
from django.http import Http404


def strp_github_standard_time(timestamp: str):
    return timestamp_str_to_tz_aware_datetime(
        timestamp=timestamp,
        dt_format=GITHUB_DATETIME_FORMAT,
        zone_name=GITHUB_DEFAULT_TIMEZONE,
    )


def upload_readme(api, repo_full_name, readme_text):
    readme_path = f"repos/{repo_full_name}/contents/README.md"
    try:
        response = api.request(readme_path, json=False)
    except Http404:
        # it doesn't exist. Create it
        response = api.put(
            readme_path,
            {
                "message": "Added README.md",
                "content": base64.b64encode(readme_text.encode("utf-8")).decode(
                    "utf-8"
                ),
            },
            json=False,
        )

    assert str(response.status_code).startswith("2"), f"{response}\n {response.json()}"


def create_org_repo(api, repo_full_name, private=True, exists_ok=False, **post_kwargs):
    (org, repo) = repo_full_name.split("/")
    args = {
        "name": repo,
        "private": private,
        # "scopes": ["repo"],
    }
    args.update(post_kwargs)
    result = api.post(f"orgs/{org}/repos", args)

    if "errors" in result:
        if result["errors"][0]["message"] == "name already exists on this account":
            if not exists_ok:
                raise Exception(result)
        else:
            # unhandled error
            print("===============")
            print(args)
            print("================")
            raise Exception(result)

    return fetch_and_save_repo(repo_full_name=repo_full_name, api=api)


def _protection_settings(restrictions_users=None, restrictions_teams=None):
    restrictions_users = restrictions_users or []
    restrictions_teams = restrictions_teams or []
    return {
        "required_status_checks": None,
        "enforce_admins": False,
        "required_pull_request_reviews": {
            "dismissal_restrictions": {},
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 2,
        },
        "dismissal_restrictions": {
            "users": restrictions_users,
            "teams": restrictions_teams,
        },
        # "restrictions": {"users": restrictions_users, "teams": restrictions_teams,},
        "restrictions": None,
    }


def protect_master(api, repo_full_name):
    response = api.put(
        f"repos/{repo_full_name}/branches/main/protection",
        _protection_settings(),
        headers={"Accept": "application/vnd.github.luke-cage-preview+json"},
    )
    # {'message': "If you would like to help us test the Require Multiple Reviewers API during its preview period, you must specify a custom media type in the 'Accept' header. Please see the docs for full details.", 'documentation_url': 'https://developer.github.com/v3/repos/branches/#update-branch-protection'}
    if "errors" in response:
        raise Exception(response)


def get_repo(repo_full_name, github_auth_login="", api=None, response404=None):
    api = api or Api(github_auth_login)
    return api.request(f"repos/{repo_full_name}", response404=response404)


def add_collaborator(api, repo_full_name, github_user_name, github_auth_login=None):
    api = api or Api(github_auth_login)

    response = api.put(
        f"repos/{repo_full_name}/collaborators/{github_user_name}",
        {"permission": "push"},
        json=False,
    )

    if response.status_code == 404:
        return  # TODO
        raise Exception(f"user or repo not found: {repo_full_name} {github_user_name}")

    if response.status_code not in [201, 204]:
        raise Exception(response.content)

    # collaborators = get_collaborators(github_auth_login, repo_full_name, api=api)

    # if github_user_name not in collaborators:
    # EXCEPTION is always raised because collaborators is a list of dictionaries and github_user_name is a stringz
    #     raise Exception(f"Adding collaborator: {github_user_name} unsuccessful.")


# def create_repo(github_auth_login, repo_full_name, github_user_name, readme_text, api):
#     api = api or Api(github_auth_login)

#     create_org_repo(api, repo_full_name, exists_ok=True, private=True)
#     # upload_readme(api, repo_full_name, readme_text)
#     protect_master(api, repo_full_name)


# def create_repo_and_assign_contributer(
#     github_auth_login, repo_full_name, github_user_name, readme_text, api=None
# ):
#     create_repo(github_auth_login, repo_full_name, github_user_name, readme_text, api)
#     add_collaborator(
#         api, repo_full_name, github_user_name, github_auth_login=github_auth_login
#     )


def save_repo(repo: dict, user=None):
    print(f"saving: {repo['full_name']}")

    obj, created = models.Repository.objects.get_or_create(
        ssh_url=repo["ssh_url"],
        defaults={
            "full_name": repo["full_name"],
            "owner": repo["owner"]["login"],
            "ssh_url": repo["ssh_url"],
            "private": repo["private"],
            "created_at": strp_github_standard_time(
                repo["created_at"],
            ),
            "archived": repo["archived"],
            "user": user,
        },
    )

    if not created:
        obj.archived = obj.archived or repo["archived"]
        obj.save()
    return obj


def fetch_and_save_repo(api, repo_full_name):
    repo_dict = get_repo(api=api, repo_full_name=repo_full_name, response404=404)
    if repo_dict == 404:
        return
    o = save_repo(repo_dict)
    assert o != None
    return o


# def create_webhooks(api):
#     api.post(
#         f"repos/{owner}/{repo}/hooks",
#         headers={"accept": "application/vnd.github.v3+json"},
#         data={
#             'config': {
#                 'url' :
#                 'content_type' : 'json',
#                 'events': [
#                     # https://docs.github.com/en/developers/webhooks-and-events/github-event-types
#                     'PullRequestEvent','PullRequestReviewCommentEvent','PushEvent']
#             }
#         },
#     )
