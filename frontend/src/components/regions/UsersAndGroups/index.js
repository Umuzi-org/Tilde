import React from "react";
import { connect } from "react-redux";
import Presentation from "./Presentation.js";
import { apiReduxApps } from "../../../apiAccess/redux/apiApps";
// import operations from "./redux/operations.js";

import useMaterialUiFormState from "../../../utils/useMaterialUiFormState";

function cleanAndFilterUserGroups(userGroups, filterBy) {
  let ret = Object.values(userGroups);
  ret.sort((a, b) => (a.name > b.name ? 1 : -1));
  if (filterBy) {
    return ret.filter((group) => group.name.indexOf(filterBy) !== -1);
  }
  return ret;
}

function cleanAndFilterUsers(userGroups, filterBy) {
  let users = {};

  for (let group of Object.values(userGroups)) {
    for (let member of group.members) {
      const email = member.userEmail;

      if (filterBy && email.indexOf(filterBy) === -1) continue;

      users[email] = {
        ...users[email],
        userId: member.userId,
      };
      users[email].groups = {
        ...users[email].groups,
        [group.name]: {
          groupId: group.id,
          ...member,
        },
      };
    }
  }
  return users;
}

function UsersAndGroupsUnconnected({ fetchUserGroupsPages, userGroups }) {
  const [
    formState,
    { filterByGroup, filterByUser },
    formErrors,
    dataFromState,
  ] = useMaterialUiFormState({
    filterByGroup: {},
    filterByUser: {},
  });

  const props = {
    userGroups: cleanAndFilterUserGroups(userGroups, filterByGroup.value),
    users: cleanAndFilterUsers(userGroups, filterByUser.value),
    filterByGroup,
    filterByUser,
  };

  React.useEffect(() => {
    fetchUserGroupsPages({
      dataSequence: [{ page: 1 }, { page: 2 }],
    });
  });

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    userGroups: state.Entities.userGroups || {},
  };
};

const mapDispatchToProps = (dispatch) => {
  const fetchUserGroupsPages = ({ dataSequence }) => {
    dispatch(
      apiReduxApps.FETCH_USER_GROUPS_PAGE.operations.maybeStartCallSequence({
        dataSequence,
      })
    );
  };

  return {
    fetchUserGroupsPages,
  };
};

const UsersAndGroups = connect(
  mapStateToProps,
  mapDispatchToProps
)(UsersAndGroupsUnconnected);

export default UsersAndGroups;
