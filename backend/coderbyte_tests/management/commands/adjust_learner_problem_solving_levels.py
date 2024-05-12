"""
Look at the last 3 tests for each active learner. If the last 3 tests are all above 80% then increase their problem solving level by 1. If the last 3 tests are all below 50% then decrease their problem solving level by 1.
"""

from django.core.management.base import BaseCommand
from coderbyte_tests.models import CoderbyteTestResult
from django.contrib.auth import get_user_model
from django.db.models import Q
from core.models import Team
import re
from coderbyte_tests.constants import PROBLEM_SOLVING_TEAM_NAME_START


User = get_user_model()


def _get_current_psf_level_for_user(user):
    team = _get_current_psf_team_for_user(user)
    if team:
        return _get_psf_level_from_team(team)


def _get_psf_level_from_team(team):
    return int(team.name.split()[-1])


def _remove_user_from_lower_psf_team(teams, user):
    # breakpoint()
    team_levels = [(_get_psf_level_from_team(team), team) for team in teams]
    team_levels.sort()  # sorts by the first element in each tuple, so the smaller number is first
    for level, team in team_levels[:-1]:
        team.user_set.remove(user)


def _get_current_psf_team_for_user(user):
    teams = [
        o.team
        for o in user.groups.filter(
            name__startswith=PROBLEM_SOLVING_TEAM_NAME_START
        ).prefetch_related("team")
    ]
    if len(teams) == 0:
        return None

    if len(teams) > 1:
        # something was misconfigured by a human. Aarg
        _remove_user_from_lower_psf_team(teams, user)
        return _get_current_psf_team_for_user(user)
    return teams[0]


def _get_psf_team_from_level(level: int):
    full_team_name = f"{PROBLEM_SOLVING_TEAM_NAME_START} {level}"
    return Team.objects.get(name=full_team_name)


def _set_learner_problem_solving_level(user, new_level):
    # breakpoint()
    new_level = max([new_level, 0])  # cant be less than 0
    new_level = min([new_level, 3])  # cant be more than 3
    print(f"changing user level to {new_level}")

    current_team = _get_current_psf_team_for_user(user)
    current_level = _get_psf_level_from_team(current_team)

    if current_level == new_level:
        return  # noting to do

    new_team = _get_psf_team_from_level(new_level)

    current_team.user_set.remove(user)
    new_team.user_set.add(user)


def _get_level_from_test_name(name):
    """
    eg 'Problem solving 0.8' => 0
        'Problem solving foundation 2.4'
    """
    found = re.search("Problem solving (foundation )?(?P<level>\d)\.\d+", name)
    if not found:
        breakpoint()
    if found:
        return int(found.group("level")[0])


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.filter(active=True).filter(
            groups__name__startswith=PROBLEM_SOLVING_TEAM_NAME_START
        )

        total = users.count()
        for i, user in enumerate(users):
            print(f"{i+1}/{total}: {user.email}")
            current_level = _get_current_psf_level_for_user(user)
            if current_level == None:
                breakpoint()
            assert current_level != None

            test_results = (
                CoderbyteTestResult.objects.filter(user=user)
                .filter(
                    Q(status=CoderbyteTestResult.STATUS_SUBMITTED)
                    | Q(status=CoderbyteTestResult.STATUS_TIME_EXPIRED)
                )
                .filter(assessment_name__startswith="Problem solving")
                .order_by("-date_joined")[:3]
            )

            if len(test_results) < 3:
                # not enough info for this user
                print("not enough tests")
                continue

            test_levels = [
                _get_level_from_test_name(result.assessment_name)
                for result in test_results
            ]
            print(f"test levels: {test_levels}")

            unique_test_levels = set(test_levels)
            if len(unique_test_levels) > 1:
                # the learner must have changed levels recently
                continue

            test_level = test_levels[0]

            if test_level < current_level:
                print(
                    f"test level {test_level} is less than user current level {current_level}"
                )
                # eg the learner passed a bunch of level 0 tests, but they are level 1 currently. They must have levelled up recently
                continue

            # now get the scores. If there was plagiarism the score is zero
            for result in test_results:
                if result.plagiarism == None:
                    breakpoint()
                    # expect this to always have a value

            scores = [
                (
                    result.final_score
                    if result.plagiarism == CoderbyteTestResult.PLAGIARISM_NOT_DETECTED
                    else 0
                )
                for result in test_results
            ]
            print(f"final scores = {scores}")

            if all([score > 80 for score in scores]):
                _set_learner_problem_solving_level(user, current_level + 1)
            elif all([score < 50 for score in scores]):
                _set_learner_problem_solving_level(user, current_level - 1)
