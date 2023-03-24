from core import models as core_models
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

        self.__response_cache = {}

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
        print(f"PUT {full_url}")

        response = requests.put(full_url, headers=self.headers(headers), json=data)

        if json:
            return response.json()
        return response

    def delete(self, url_end, headers=None, json=True):
        full_url = f"{GITHUB_BASE_URL}/{url_end}"

        response = requests.delete(full_url, headers=self.headers(headers))

        if json:
            return response.json()
        return response

    def post(self, url_end, data, headers=None):
        full_url = f"{GITHUB_BASE_URL}/{url_end}"

        response = requests.post(full_url, headers=self.headers(headers), json=data)

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
        if response.status_code == 404:
            from django.http import Http404

            raise Http404()
        assert (
            response.status_code == 200
        ), f"{response.status_code} {response.text} {response.reason}"
        if json:
            return response.json()
        return response

    def request_pages(self, url_end, response404=None, params=None, headers=None):
        params = params or {}
        params["page"] = 1
        fetched_list = []
        while fetched_list or (params["page"] == 1):
            fetched_list = self.request(
                f"{url_end}?{urlencode(params)}",
                response404=response404,
                headers=headers,
            )
            if response404 and fetched_list == response404:
                return response404
            for item in fetched_list:
                yield item
            params["page"] += 1

    def team_exists(self, organisation_name: str, team_name: str) -> bool:
        # result = self.request(
        #     f"orgs/{organisation_name}/teams/{team_name}",
        #     headers={"accept": "application/vnd.github.v3+json"},
        # ) #todo: rather just get the one team and see if it exists
        teams = self.list_organisation_teams(organisation_name)

        for team in teams:
            if team["name"] == team_name:
                return True
        return False

    def create_team(
        self, organisation_name, team_name, description="Automatically generated team"
    ):
        if not self.team_exists(organisation_name, team_name):

            result = self.post(
                f"orgs/{organisation_name}/teams",
                data={"description": description, "name": team_name},
                headers={"accept": "application/vnd.github.v3+json"},
            )

            # assert "name" in result, f"result = {result}"
            # assert result["name"] == team_name, f"result = {result}"

    def clear_failed_organisation_invites(self, organisation_name: str):
        failed_invitations = self.request_pages(
            f"orgs/{organisation_name}/failed_invitations",
            headers={"accept": "application/vnd.github.v3+json"},
        )

        for invitation in failed_invitations:
            breakpoint()
            pass
            response = self.delete(
                f"orgs/{organisation_name}/invitations/{invitation_id}"
            )
            breakpoint()
            pass

    def list_organisation_teams(self, organisation_name):
        self.__response_cache["list_organisation_teams"] = self.__response_cache.get(
            "list_organisation_teams", {}
        )

        teams = self.__response_cache["list_organisation_teams"].get(organisation_name)
        if teams is None:
            result = self.request_pages(f"orgs/{organisation_name}/teams")
            self.__response_cache["list_organisation_teams"][organisation_name] = [
                d for d in result
            ]

        return self.__response_cache["list_organisation_teams"][organisation_name]

    def list_organisation_members(self, organisation_name):
        self.__response_cache["list_organisation_members"] = self.__response_cache.get(
            "list_organisation_members", {}
        )

        members = self.__response_cache["list_organisation_members"].get(
            organisation_name
        )
        if members is None:
            result = self.request_pages(f"orgs/{organisation_name}/members")
            self.__response_cache["list_organisation_members"][organisation_name] = [
                d for d in result
            ]
        return self.__response_cache["list_organisation_members"][organisation_name]

    def list_pending_organisation_invitations(self, organisation_name):
        self.__response_cache[
            "list_pending_organisation_invitations"
        ] = self.__response_cache.get("list_pending_organisation_invitations", {})

        members = self.__response_cache["list_pending_organisation_invitations"].get(
            organisation_name
        )
        if members is None:
            result = self.request_pages(f"orgs/{organisation_name}/invitations")
            self.__response_cache["list_pending_organisation_invitations"][
                organisation_name
            ] = [d for d in result]
        return self.__response_cache["list_pending_organisation_invitations"][
            organisation_name
        ]

    def user_is_org_member(self, organisation_name: str, github_name: str) -> bool:
        members = self.list_organisation_members(organisation_name)
        for member in members:
            if member["login"] == github_name:
                return True
        return False

    def organisation_invitation_pending(
        self, organisation_name: str, github_name: str
    ) -> bool:
        invitations = self.list_pending_organisation_invitations(organisation_name)
        for invitation in invitations:
            if invitation["login"] == github_name:
                return True
        return False

    def add_user_to_org_return_accepted(
        self, organisation_name: str, github_name: str
    ) -> bool:
        """if the user is in the org already then return True, but if they have an invite that is not yet accepted return False"""
        if self.user_is_org_member(organisation_name, github_name):
            return True
        if not self.organisation_invitation_pending(organisation_name, github_name):
            response = self.put(
                f"orgs/{organisation_name}/memberships/{github_name}",
                headers={"accept": "application/vnd.github.v3+json"},
                data={},
            )
            assert "state" in response, response
            assert response["state"] in ["pending", "active"], response
        return False

    def add_user_to_team(self, organisation_name, team_name, github_name):
        is_member = self.add_user_to_org_return_accepted(organisation_name, github_name)

        if is_member:
            response = self.put(
                f"orgs/{organisation_name}/teams/{team_name.replace(' ','-')}/memberships/{github_name}",
                headers={"accept": "application/vnd.github.v3+json"},
                data={},
            )
            if not (response.get("state") == "active"):
                breakpoint()

            assert response["state"] == "active", response

    def user_exists(self, github_name):
        final_url = f"https://github.com/{github_name}"
        if requests.get(final_url).status_code == 404:
            return False
        return True


# TODO: no response404 args. Rather raise 404 exceptions
# TODO: check response codes on responses. They should be 2XX or raise exceptions
# TODO: depricate request method. It should be called `get` for get requests
