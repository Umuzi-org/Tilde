from coderbyte_tests.constants import PROBLEM_SOLVING_TEAM_NAME_START


def get_current_psf_level_for_user(user):
    team = get_current_psf_team_for_user(user)
    if team:
        return get_psf_level_from_team(team)


def get_psf_level_from_team(team):
    return int(team.name.split()[-1])


def get_current_psf_team_for_user(user):
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
        return get_current_psf_team_for_user(user)
    return teams[0]


def _remove_user_from_lower_psf_team(teams, user):
    # breakpoint()
    team_levels = [(get_psf_level_from_team(team), team) for team in teams]
    team_levels.sort()  # sorts by the first element in each tuple, so the smaller number is first
    for level, team in team_levels[:-1]:
        team.user_set.remove(user)
