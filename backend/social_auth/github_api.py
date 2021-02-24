from core import models as core_models
from git_real import models
from social_auth import models as social_models
from git_real.constants import GITHUB_BASE_URL
import requests
from django.utils.http import urlencode


class Api:
    def __init__(self, github_name=None, github_token=None):
        if github_token:
            self.token = github_token
        else:
            self.token = self.get_auth_token(github_name)
        assert self.token

    def who_am_i(self):
        response = self.request("user")
        #         keys()
        # dict_keys(['login', 'id', 'node_id', 'avatar_url', 'gravatar_id', 'url', 'html_url', 'followers_url', 'following_url', 'gists_url', 'starred_url', 'subscriptions_url', 'organizations_url', 'repos_url', 'events_url', 'received_events_url', 'type', 'site_admin', 'name', 'company', 'blog', 'location', 'email', 'hireable', 'bio', 'public_repos', 'public_gists', 'followers', 'following', 'created_at', 'updated_at'])
        return {"github_name": response["login"], "raw": response}

    def get_auth_token(self, github_name):
        assert (
            github_name
        ), f"github_name cannot be falsey, {github_name} {type(github_name)}"
        try:
            user = core_models.User.objects.get(social_profile__github_name=github_name)
        except core_models.User.DoesNotExist:
            raise Exception(
                f"Cannot find user with github username '{github_name}'. Are you sure it's in the database?"
            )

        try:
            token = social_models.GithubOAuthToken.objects.get(user=user)
        except social_models.GithubOAuthToken.DoesNotExist:
            raise Exception(
                "Cannot find matching github auth token - are you sure you have looged in?"
            )

        return token.access_token

    def headers(self, headers=None):
        result = {
            "Accept": "application/vnd.github.nebula-preview+json",
            "Authorization": f"token {self.token}",
        }
        result.update(headers or {})
        return result

    def put(self, url_end, data, headers=None, json=True):
        full_url = f"{GITHUB_BASE_URL}/{url_end}"

        response = requests.put(full_url, headers=self.headers(headers), json=data)

        if json:
            return response.json()
        return response

    def delete(self, url_end, headers=None, json=True):
        full_url = f"{GITHUB_BASE_URL}/{url_end}"
        print(full_url)

        response = requests.delete(full_url, headers=self.headers(headers))

        if json:
            return response.json()
        return response

    def post(self, url_end, data):
        full_url = f"{GITHUB_BASE_URL}/{url_end}"

        response = requests.post(full_url, headers=self.headers(), json=data)

        return response.json()

    def request(self, url_end, response404=None, json=True, headers=None):

        full_url = f"{GITHUB_BASE_URL}/{url_end}"

        print(f"curl {full_url}")

        response = requests.get(full_url, headers=self.headers(headers))

        if (response404 is not None) and response.status_code == 404:
            with open("misspellings.log", "a") as f:
                f.write(url_end)  # TODO: refactor. put this somewhere else
                f.write("\n")
            return response404
        assert (
            response.status_code == 200
        ), f"{response.status_code} {response.text} {response.reason}"
        if json:
            return response.json()
        return response

    def request_pages(self, url_end, response404=None, params=None):
        params = params or {}
        params["page"] = 1
        fetched_list = []
        while fetched_list or (params["page"] == 1):
            fetched_list = self.request(f"{url_end}?{urlencode(params)}", response404)
            if response404 and fetched_list == response404:
                return response404
            for item in fetched_list:
                yield item
            params["page"] += 1


# TODO: no response404 args. Rather raise 404 exceptions
