import random
import string
import os
from django.contrib.auth.decorators import login_required
from django.utils.http import urlencode
from django.http import HttpResponseRedirect
from social_auth.github_api import Api
import json
from apiclient import discovery
from oauth2client import client
import httplib2

from django.http import JsonResponse
import requests

from . import models
from . import constants
from . import serializers
from . import google_helpers

from core import serializers as core_serializers
from core import helpers as core_helpers
from core import constants as core_constants

from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import viewsets, status


OAUTH_STATE = "oauth_state"

# Github oauth flow based on:
# https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/


@login_required
def authorize_github_start(request):

    request.session[OAUTH_STATE] = "".join(
        random.choices(string.digits + string.ascii_letters, k=15)
    )

    get_parameters = urlencode(
        {
            "client_id": os.environ["GITHUB_CLIENT_ID"],
            # "login": request.user.user_profile.github_name,
            "scope": "repo",
            "state": request.session[OAUTH_STATE],
        }
    )

    return HttpResponseRedirect(
        "https://github.com/login/oauth/authorize?" + get_parameters
    )


@login_required
def authorize_github_callback(request):

    code = request.GET["code"]
    state = request.GET["state"]

    assert state == request.session[OAUTH_STATE]
    data = {
        "client_id": os.environ["GITHUB_CLIENT_ID"],
        "client_secret": os.environ["GITHUB_CLIENT_SECRET"],
        "code": code,
        "state": state,
    }

    response = requests.post(
        "https://github.com/login/oauth/access_token",
        json=data,
        headers={"Accept": "application/json"},
    )
    assert (
        response.status_code == 200
    ), "Unexpected response {response.status_code}\n{response.content}"

    response_data = response.json()

    if "error" in response_data:
        return JsonResponse(response_data)

    # save the credentials in the db
    token, created = models.GithubOAuthToken.objects.get_or_create(
        user=request.user, defaults=response_data
    )
    if not created:
        token.update(**response_data)
        token.save()

    # get the username

    api = Api(github_token=token.access_token)
    github_name = api.who_am_i()["github_name"]

    profile, created = models.SocialProfile.objects.get_or_create(
        user=request.user, github_name=github_name
    )
    if not created:
        profile.github_name = github_name
        profile.save()

    return JsonResponse(
        {"status": "OK", "message": f"Github username set to {github_name}"}
    )


@api_view(["post"])
def oauth_one_time_token_auth(request):
    """based on https://developers.google.com/identity/sign-in/web/server-side-flow"""

    print("start")
    serializer = serializers.OAuthOneTimeTokenSerialiser(data=request.data)
    if serializer.is_valid():
        print("serialiser is valid")
        provider = serializer.data.get("provider")
        if provider == "google":
            return google_oauth_one_time_token_auth(
                auth_code=serializer.data.get("code")
            )
        else:
            raise Exception(f"Unhandled provider: {provider}")
    else:
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


def google_oauth_one_time_token_auth(auth_code):
    print(f"google_oauth_one_time_token_auth {auth_code}")

    email = google_helpers.get_email_from_one_time_code(auth_code)
    print(email)

    token, user_created = core_helpers.get_auth_token_for_email(email)

    if token is not None:
        print("got a token")
        serialiser = core_serializers.WhoAmISerializer(token)
        if user_created:
            return Response(serialiser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialiser.data)
    else:
        print("cant log in with this user")
        serialiser = core_serializers.UserErrorSerialiser(
            data={
                "message": f"Please log in with your @{core_constants.BUSINESS_EMAIL_DOMAIN} email address if you have one. Otherwise please talk to an administrator to hook you up"
            }
        )
        assert serialiser.is_valid(), serialiser.errors
        return Response(serialiser.data, status=status.HTTP_401_UNAUTHORIZED)
