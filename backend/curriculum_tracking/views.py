from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import BulkAddLearnersToTeamForm
from .helpers import add_users_to_team, remove_leading_and_trailing_whitespace
from django.contrib import messages

# need some nudges in the right direction
# TODO: add a new form page as part of django admin
# TODO: add a link to navigate to new form page
# TODO: style new form page like django admin if not already styled

# shoul be fine
# TODO: sanitize email_addresses to be a list instead of string
# TODO: sanitize team_name


def bulk_add_learners_to_team(request):
    if request.method == "POST":
        team_name = request.POST["team_name"]
        email_addresses = request.POST["email_addresses"]
        form = BulkAddLearnersToTeamForm(request.POST)
        if form.is_valid():
            team_name = remove_leading_and_trailing_whitespace(team_name)
            add_users_to_team(team_name, [email_addresses])
            messages.success(request, "You have successfully added learners to a team")
            return redirect("bulk_add_learners_to_team")
    else:
        form = BulkAddLearnersToTeamForm()

    context = {"form": form}
    return render(request, "admin/bulk_add_learners_to_team.html", context)
