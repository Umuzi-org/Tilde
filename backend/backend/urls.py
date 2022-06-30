"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from rest_framework import routers
from core import views as core_views
from curriculum_tracking import api_views as curriculum_tracking_api_views
from activity_log import api_views as activity_log_api_views


# from rest_framework.schemas import get_schema_view

# schema_view = get_schema_view(title="Tilde")


router = routers.DefaultRouter()
router.register(r"users", core_views.UserViewSet, "user")
router.register(r"user_profiles", core_views.UserProfileViewSet, "userprofile")
router.register(r"curriculums", core_views.CurriculumViewSet, "curriculum")


router.register(r"teams", core_views.TeamViewSet, "team")


router.register(
    r"management_actions",
    curriculum_tracking_api_views.ManagementActionsViewSet,
    "managementaction-list",
)

router.register(
    r"recruit_projects",
    curriculum_tracking_api_views.RecruitProjectViewset,
    "recruitproject",
)

router.register(
    r"recruit_project_reviews",
    curriculum_tracking_api_views.RecruitProjectReviewViewset,
    "recruitprojectreview",
)

router.register(
    r"content_item",
    curriculum_tracking_api_views.ContentItemViewset,
    "contentitem",
)

router.register(
    r"content_item_order",
    curriculum_tracking_api_views.ContentItemOrderViewset,
    "contentitemorder",
)

router.register(
    r"agile_card",
    curriculum_tracking_api_views.AgileCardViewset,
    "agilecard",
)

router.register(
    r"repository",
    curriculum_tracking_api_views.RepositoryViewset,
    "repository",
)

router.register(
    r"commit",
    curriculum_tracking_api_views.CommitViewSet,
    "commit",
)

router.register(
    r"pull_request",
    curriculum_tracking_api_views.PullRequestViewSet,
    "pullrequest",
)

router.register(
    r"pull_request_review",
    curriculum_tracking_api_views.PullRequestReviewViewSet,
    "pullrequestreview",
)

router.register(
    r"card_summaries",
    curriculum_tracking_api_views.CardSummaryViewset,
    "cardsummary",
)

router.register(
    r"topic_reviews",
    curriculum_tracking_api_views.TopicReviewViewset,
    "topicreview",
)

router.register(
    r"topic_progress",
    curriculum_tracking_api_views.TopicProgressViewset,
    "topicprogress",
)

router.register(
    r"workshop_attendance",
    curriculum_tracking_api_views.WorkshopAttendanceViewset,
    "workshopattendance",
)

router.register(
    r"review_trust",
    curriculum_tracking_api_views.ReviewTrustsViewSet,
    "reviewtrust",
)

router.register(
    r"burndown_snap_shot",
    curriculum_tracking_api_views.BurnDownSnapShotViewset,
    "burndownsnapshot",
)

router.register(
    r"activity_log_day_count",
    activity_log_api_views.ActivityLogDayCountViewset,
    "activitylogdaycount",
)

router.register(
    r"event_type",
    activity_log_api_views.EventTypeViewSet,
    "eventtype",
)

# router.register(
#     r"agile_card_add_review",
#     curriculum_tracking_api_views.AgileCardInteractionAddReview,
#     "agilecardaddreview",
# )

# router.register(
#     r"/user/<int:user_id>/projects",
#     curriculum_tracking_api_views.RecruitProjectList,
#     "user-recrtuitprojects",
# )

router.register(
    r"stream_registration",
    core_views.StreamRegistrationViewset,
    "streamregistration",
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/", include(router.urls)),
    path("api/", include("core.urls")),
    path("api/dj-rest-auth/", include("dj_rest_auth.urls")),
    # path("api/schema", schema_view),
    path("git_real/", include("git_real.urls")),
    path("social_auth/", include("social_auth.urls")),
    # path("api/", include("curriculum_tracking.api_urls")),

    path(
        "password_reset_confirm/<uidb64>/<token>/",
        lambda *a, **k: None,  # we don't actually need a view here. We redirect to the frontend
        name="password_reset_confirm",
    ),
]
