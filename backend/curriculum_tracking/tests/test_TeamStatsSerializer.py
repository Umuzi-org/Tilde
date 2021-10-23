from core import models
from curriculum_tracking.serializers import TeamStatsSerializer
from django.test import TestCase
from . import factories
from git_real.tests.factories import PullRequestFactory
from core.tests.factories import TeamFactory, UserFactory
from django.utils import timezone


class TeamStatsSerializerTests(TestCase):
    def setUp(self) -> None:
        self.team1 = TeamFactory()
        self.team2 = TeamFactory()
        team1_users = [UserFactory() for _ in range(2)]
        self.team1.user_set.set(team1_users)
        self.team2.user_set.set([UserFactory() for _ in range(2)])

        now = timezone.now()
        times = [now - timezone.timedelta(hours=n) for n in range(3, 0, -1)]

        # the following relationship holds true for any two times in the list
        assert times[0] < times[1]  # times[0] is older than times[1]
        # asserts are nice for sanity checking and code as documentation

        # add a few random cards and prs
        for _ in range(3):
            card = factories.AgileCardFactory()
            card.recruit_project.request_review()
            PullRequestFactory(repository=card.recruit_project.repository)

        prs = []
        review_cards = []

        # now set up cards and prs for team1 users. These will be represented in the serializer data
        for n in range(2):
            # 2 cards per person, one is in review, one is in progress
            ip_card = factories.AgileCardFactory(assignees=[team1_users[n]])
            review_card = factories.AgileCardFactory(assignees=[team1_users[n]])
            review_card.recruit_project.request_review(force_timestamp=times[n])

            review_cards.append(review_card)

            # and one PR per person
            pr = PullRequestFactory(
                repository=ip_card.recruit_project.repository, created_at=times[n]
            )
            prs.append(pr)

        self.oldest_pr = prs[0]  # these are in chronological order
        self.oldest_review_card = review_cards[0]

    def test_oldest_open_pr_time(self):
        response1 = TeamStatsSerializer(self.team1).data
        response2 = TeamStatsSerializer(self.team2).data

        self.assertEqual(response1["oldest_open_pr_time"], self.oldest_pr.created_at)
        self.assertEqual(response2["oldest_open_pr_time"], None)

    def test_total_open_prs(self):
        response1 = TeamStatsSerializer(self.team1).data
        response2 = TeamStatsSerializer(self.team2).data

        self.assertEqual(response1["total_open_prs"], 2)
        self.assertEqual(response2["total_open_prs"], 0)

    def test_oldest_card_in_review_time(self):
        response1 = TeamStatsSerializer(self.team1).data
        response2 = TeamStatsSerializer(self.team2).data

        self.assertEqual(
            response1["oldest_card_in_review_time"],
            self.oldest_review_card.review_request_time,
        )
        self.assertEqual(response2["oldest_card_in_review_time"], None)

    def test_total_cards_in_review(self):
        response1 = TeamStatsSerializer(self.team1).data
        response2 = TeamStatsSerializer(self.team2).data

        self.assertEqual(response1["total_cards_in_review"], 2)
        self.assertEqual(response2["total_cards_in_review"], 0)
