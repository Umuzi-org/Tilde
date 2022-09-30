import React from "react";
import { connect } from "react-redux";
import Presentation from "./Presentation.jsx";
import { apiReduxApps } from "../../../apiAccess/apiApps";

// import useMaterialUiFormState from "../../../utils/useMaterialUiFormState";

import { apiUtilitiesOperations } from "../../../apiAccess/redux";

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

export function cleanAndFilterUsers(teams, filterBy, filterUsersByGroupName) {
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
      users[email].groups = {
        ...users[email].groups,
        [group.name]: {
          teamId: group.id,
          ...member,
        },
      };
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
  const [filterUsersByGroupName, setFilterUsersByGroupName] = React.useState(
    ""
  );

  const [filterFormValues, setFilterFormValues] = React.useState({
    team: "",
    user: "",
  });

  const handleUserGroupClick = (name) => {
    if (name === filterUsersByGroupName) setFilterUsersByGroupName("");
    else setFilterUsersByGroupName(name);
  };

  function handleChangeFilterFormInput(name) {
    function handler(event) {
      setFilterFormValues({
        ...filterFormValues,
        [name]: event.target.value,
      });
    }
    return handler;
  }

  const props = {
    teams: cleanAndFilterTeams({
      teams,
      filterBy: filterFormValues.team,
    }),
    users: cleanAndFilterUsers(
      teams,
      filterFormValues.user,
      filterUsersByGroupName
    ),
    teamSummaryStats,

    filterUsersByGroupName,
    handleUserGroupClick,
    filterFormValues,
    handleChangeFilterFormInput,
  };

  React.useEffect(() => {
    fetchTeamsPages();
    fetchTeamSummaryStatsPages();
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
  return {
    fetchTeamsPages: () => {
      const data = { page: 1 };
      dispatch(
        apiReduxApps.FETCH_TEAMS_PAGE.operations.maybeStart({
          data,

          successDispatchActions: [
            apiUtilitiesOperations.fetchAllPages({
              API_BASE_TYPE: "FETCH_TEAMS_PAGE",
              requestData: data,
            }),
          ],
        })
      );
    },

    fetchTeamSummaryStatsPages: () => {
      const data = { page: 1 };
      dispatch(
        apiReduxApps.FETCH_TEAM_SUMMARY_STATS_PAGE.operations.maybeStart({
          data,
          successDispatchActions: [
            apiUtilitiesOperations.fetchAllPages({
              API_BASE_TYPE: "FETCH_TEAM_SUMMARY_STATS_PAGE",
              requestData: data,
            }),
          ],
        })
      );
    },
  };
}

const UsersAndGroups = connect(
  mapStateToProps,
  mapDispatchToProps
)(UsersAndGroupsUnconnected);

export default UsersAndGroups;
