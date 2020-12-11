from django.shortcuts import render
from rest_framework import viewsets
from core.forms import TeamForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import resolve
import datetime
from core.models import Cohort, ProductTeam
from django.contrib.auth import get_user_model
from . import models

# from pprint import pprint

User = get_user_model()

LATE = "LATE"
ON_TIME = "ON_TIME"

DAYS_PAST = 14

# TODO: this whole file is not DRY

# from attendance.serializers import AttendanceSerializer
# from attendance.models import Attendance

# Create your views here.

# class AttendanceView(viewsets.ModelViewSet):
#     serializer_class = AttendanceSerializer
#     queryset = Attendance.objects.all()


def index(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            cohort_id = form.cleaned_data["cohort"]
            product_team_id = form.cleaned_data["product_team"]
            staff = form.cleaned_data["staff"]
            everyone = form.cleaned_data.get("everyone")

            if cohort_id:
                url = reverse("cohort_attendance", kwargs={"id": cohort_id})
            if product_team_id:
                url = reverse("product_attendance", kwargs={"id": product_team_id})
            if staff:
                url = reverse("staff_attendance")
            if everyone:
                url = reverse("all_attendance")

            return HttpResponseRedirect(url)
    else:
        form = TeamForm()
    return render(request, "attendance/select_team.html", {"form": form})


def _entry_score_to_label(row):
    return {1: LATE, 2: ON_TIME}[row["score"]]


def _return_graph_response(request, heading, attendance_querysets, users):
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd

    columns = [
        "timestamp",
        "user.email",
        "plan_of_action",
        "problems",
        "comments",
        "late_reason",
        "score",
        "still_on_track",
        "_index",
        "_weight",
        "_type",
        "_user.active",
    ]

    row_dicts = []
    for queryset in attendance_querysets:
        row_dicts.extend([o.graph_dict() for o in queryset])

    if len(row_dicts) == 0:
        from django.http import HttpResponse

        return HttpResponse(
            "Nothing to see here! Come back in half an hour and take another look"
        )

    #      = (
    #     [o.graph_dict() for o in morning]
    #     + [o.graph_dict() for o in afternoon]
    #     + [o.graph_dict() for o in evening]
    # )

    for row in row_dicts:
        # the more they have to say, the bigger the dot

        row["_weight"] = (
            len(
                row.get("late_reason", "")
                + row.get("plan_of_action", "")
                + row.get("comments", "")
                + row.get("problems", "")
            )
            + 10
        )

    rows = [[row.get(col) for col in columns] for row in row_dicts]

    df = pd.DataFrame(rows, columns=columns)

    summed = df.groupby(["user.email"])["score"].sum().sort_values()
    user_scores = summed.to_dict()  # {email address: score, ...}

    user_indexes = list(user_scores.keys())

    df["score"] = df.apply(_entry_score_to_label, axis=1)
    df["_index"] = df.apply(lambda row: user_indexes.index(row["user.email"]), axis=1)

    figure = px.scatter(
        df,
        x="timestamp",
        y="_index",
        hover_data=df.columns,
        height=800,
        size="_weight",
        color="score",
        color_discrete_map={LATE: "orange", ON_TIME: "blue"},
    )

    figure.update_layout(
        yaxis={
            "tickmode": "array",
            "tickvals": list(range(len(users))),
            "ticktext": [
                f"{email} [score = {score}]" for email, score in user_scores.items()
            ],
        },
        xaxis={
            "showticklabels": True,
        },
    )

    return render(
        request,
        "attendance/attendance_log.html",
        {"figure": figure.to_html(), "heading": heading},
    )


def cohort_attendance_graph(request, id):

    # TODO: create api endpoint for exposiong this data (#162)
    DAYS_PAST = 14

    cutoff = datetime.datetime.now() - datetime.timedelta(days=DAYS_PAST)

    cohort = Cohort.objects.get(pk=id)
    heading = f"for {cohort}"
    users = cohort.get_member_users()
    morning = models.MorningAttendance.objects.filter(
        cohort=cohort, timestamp__gte=cutoff
    )
    afternoon = models.AfternoonAttendance.objects.filter(
        cohort=cohort, timestamp__gte=cutoff
    )
    evening = models.EveningAttendance.objects.filter(
        cohort=cohort, timestamp__gte=cutoff
    )

    return _return_graph_response(
        # row_dicts=row_dicts,
        attendance_querysets=[morning, afternoon, evening],
        heading=heading,
        users=users,
        request=request,
    )


def product_attendance_graph(request, id):

    # TODO: create api endpoint for exposiong this data (#163)
    product_team = ProductTeam.objects.get(pk=id)
    heading = f"for product: {product_team}"

    cutoff = datetime.datetime.now() - datetime.timedelta(days=DAYS_PAST)
    users = product_team.get_member_users()

    morning = product_team.morning_attendace.filter(timestamp__gte=cutoff)
    afternoon = product_team.afternoon_attendace.filter(timestamp__gte=cutoff)
    evening = product_team.evening_attendace.filter(timestamp__gte=cutoff)

    return _return_graph_response(
        attendance_querysets=[morning, afternoon, evening],
        heading=heading,
        users=users,
        request=request,
    )


def staff_attendance_graph(
    request,
):
    # TODO: create api endpoint for exposiong this data (#164)
    cutoff = datetime.datetime.now() - datetime.timedelta(days=DAYS_PAST)
    users = User.objects.filter(is_staff=True)
    heading = "for staff"

    morning = models.MorningAttendance.objects.filter(
        is_staff=True, timestamp__gte=cutoff
    )
    afternoon = models.AfternoonAttendance.objects.filter(
        is_staff=True, timestamp__gte=cutoff
    )
    evening = models.EveningAttendance.objects.filter(
        is_staff=True, timestamp__gte=cutoff
    )

    return _return_graph_response(
        attendance_querysets=[morning, afternoon, evening],
        heading=heading,
        users=users,
        request=request,
    )
