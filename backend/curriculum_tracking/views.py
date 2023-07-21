from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import BulkAddLearnersToTeamForm
from .helpers import add_users_to_team
from django.contrib import messages


def bulk_add_learners_to_team(request):
    if request.method == "POST":
        print("data:", request.POST)
        team_name = request.POST["team_name"]
        email_addresses = request.POST["email_addresses"]
        form = BulkAddLearnersToTeamForm(request.POST)
        if form.is_valid():
            add_users_to_team(team_name, [email_addresses])
            messages.success(request, "You have successfully added learners to a team")
            return redirect("bulk_add_learners_to_team")
    else:
        form = BulkAddLearnersToTeamForm()

    context = {"form": form}
    return render(request, "admin/bulk_add_learners_to_team.html", context)
