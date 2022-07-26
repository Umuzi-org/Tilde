import React from "react";
import { connect } from "react-redux";
import Presentation from "./Presentation.jsx";
import { apiReduxApps } from "../../../apiAccess/apiApps";

import useMaterialUiFormState from "../../../utils/useMaterialUiFormState";

export function cleanAndFilterTeams({ teams, filterBy }) {
  let ret = Object.values(teams);
  ret.sort((a, b) => (a.name > b.name ? 1 : -1));

  if (filterBy) {
    let terms = filterBy
      .toLowerCase()
      .split(" ")
      .filter((s) => s);

    return ret.filter((group) => {
      let name = group.name.toLowerCase();
      for (let term of terms) {
        if (name.indexOf(term) === -1) return false;
      }
      return true;
    });
  }
  return ret;
}

function ignore() {}

function cleanAndFilterUsers(teams, filterBy, filterUsersByGroupName) {
  let users = {};

  for (let group of Object.values(teams)) {
    for (let member of group.members) {
      const email = member.userEmail;

      if (
        (filterBy &&
          email.toLowerCase().indexOf(filterBy.toLowerCase()) === -1) ||
        member.userActive === false
      )
        continue;

      users[email] = {
        ...users[email],
        userId: member.userId,
      };
      {
        users[email].groups = {
          ...users[email].groups,
          [group.name]: {
            teamId: group.id,
            ...member,
          },
        };
      }
    }
  }
  if (filterUsersByGroupName) {
    let usersFilteredByGroup = {};
    for (let email of Object.keys(users)) {
      if (users[email].groups[filterUsersByGroupName])
        usersFilteredByGroup[email] = users[email];
    }
    return usersFilteredByGroup;
  }

  return users;
}

function UsersAndGroupsUnconnected({
  teams,
  teamSummaryStats,
  fetchTeamsPages,
  fetchTeamSummaryStatsPages,
}) {
  const [
    formState,
    { filterByGroup, filterByUser },
    formErrors,
    dataFromState,
  ] = useMaterialUiFormState({
    filterByGroup: {},
    filterByUser: {},
  });
  const [filterUsersByGroupName, setFilterUsersByGroupName] = React.useState(
    ""
  );
  ignore(formState, formErrors, dataFromState);

  const handleUserGroupClick = (name) => {
    if (name === filterUsersByGroupName) setFilterUsersByGroupName("");
    else setFilterUsersByGroupName(name);
  };

  const props = {
    teams: cleanAndFilterTeams({
      teams,
      filterBy: filterByGroup.value,
    }),
    users: cleanAndFilterUsers(
      teams,
      filterByUser.value,
      filterUsersByGroupName
    ),
    teamSummaryStats,
    filterByGroup,
    filterByUser,
    filterUsersByGroupName,
    handleUserGroupClick,
  };

  React.useEffect(() => {
    const dataSequence = [
      { page: 1 },
      { page: 2 },
      { page: 3 },
      { page: 4 },
      { page: 5 },
      { page: 6 },
      { page: 7 },
      { page: 8 },
      { page: 9 },
      { page: 10 },
    ];

    fetchTeamsPages({
      dataSequence,
    });

    fetchTeamSummaryStatsPages({ dataSequence });
  }, [fetchTeamsPages, fetchTeamSummaryStatsPages]);

  return <Presentation {...props} />;
}

function mapStateToProps(state) {
  return {
    teams: state.apiEntities.teams || {},
    teamSummaryStats: state.apiEntities.teamSummaryStats || {},
  };
}

function mapDispatchToProps(dispatch) {
  function fetchTeamsPages({ dataSequence }) {
    dispatch(
      apiReduxApps.FETCH_TEAMS_PAGE.operations.maybeStartCallSequence({
        dataSequence,
      })
    );
  }

  function fetchTeamSummaryStatsPages({ dataSequence }) {
    dispatch(
      apiReduxApps.FETCH_TEAM_SUMMARY_STATS_PAGE.operations.maybeStartCallSequence(
        {
          dataSequence,
        }
      )
    );
  }

  return {
    fetchTeamsPages,
    fetchTeamSummaryStatsPages,
  };
}

const UsersAndGroups = connect(
  mapStateToProps,
  mapDispatchToProps
)(UsersAndGroupsUnconnected);

export default UsersAndGroups;
