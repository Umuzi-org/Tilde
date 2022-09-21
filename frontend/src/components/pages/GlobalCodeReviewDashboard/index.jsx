import React, { useEffect } from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";

import { apiReduxApps } from "../../../apiAccess/apiApps";
import { apiUtilitiesOperations } from "../../../apiAccess/redux";

import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";
import { useState } from "react";

function removeNameFromArray({ array, name }) {
  const index = array.indexOf(name);
  if (index !== -1) {
    array.splice(index, 1);
  }
  return array;
}

function GlobalCodeReviewDashboardUnconnected({
  // mapStateToProps

  competenceReviewQueueProjectsObject,
  pullRequestReviewQueueProjectsObject,
  FETCH_COMPETENCE_REVIEW_QUEUE_PAGE,
  FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE,
  teams,

  // mapDispatchToProps

  fetchCompetenceReviewQueuePage,
  fetchPullRequestReviewQueuePage,
  fetchTeamsPages,
}) {
  teams = teams || {};

  const [filterIncludeTags, setFilterIncludeTags] = useState([]);
  const [filterExcludeTags, setFilterExcludeTags] = useState([
    "technical-assessment",
  ]);

  const [filterIncludeFlavours, setFilterIncludeFlavours] = useState([]);
  const [filterExcludeFlavours, setFilterExcludeFlavours] = useState([]);

  // const [filterAssigneeTeam, setFilterAssigneeTeam] = useState([])

  useEffect(() => {
    fetchCompetenceReviewQueuePage({ page: 1 });
    fetchPullRequestReviewQueuePage({ page: 1 });
    fetchTeamsPages();
  }, [
    fetchCompetenceReviewQueuePage,
    fetchPullRequestReviewQueuePage,
    fetchTeamsPages,
  ]);

  const fetchCompetenceReviewQueueLastCall = getLatestMatchingCall({
    callLog: FETCH_COMPETENCE_REVIEW_QUEUE_PAGE,
  }) || { loading: true };

  const fetchPullRequestQueueLastCall = getLatestMatchingCall({
    callLog: FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE,
  }) || { loading: true };

  const competenceReviewQueueProjects = Object.values(
    competenceReviewQueueProjectsObject || {}
  );

  const pullRequestReviewQueueProjects = Object.values(
    pullRequestReviewQueueProjectsObject || {}
  );

  function fetchNextCompetenceReviewQueuePage() {
    const page = fetchCompetenceReviewQueueLastCall.requestData.page + 1;
    fetchCompetenceReviewQueuePage({ page });
  }

  function fetchNextPullRequestQueuePage() {
    const page = fetchPullRequestQueueLastCall.requestData.page + 1;
    fetchPullRequestReviewQueuePage({ page });
  }

  function handleChangeFilter({
    includes,
    excludes,
    setIncludes,
    setExcludes,
  }) {
    function handleChangeFlavourFilter(name) {
      function handle() {
        if (includes.includes(name)) {
          const newFilterIncludes = removeNameFromArray({
            array: includes,
            name,
          });
          setIncludes([...newFilterIncludes]);
          setExcludes([...excludes, name]);
        } else if (excludes.includes(name)) {
          const newFilterExcludes = removeNameFromArray({
            array: excludes,
            name,
          });
          setExcludes([...newFilterExcludes]);
        } else {
          setIncludes([...includes, name]);
        }
      }
      return handle;
    }
    return handleChangeFlavourFilter;
  }

  const handleChangeFlavourFilter = handleChangeFilter({
    includes: filterIncludeFlavours,
    excludes: filterExcludeFlavours,
    setIncludes: setFilterIncludeFlavours,
    setExcludes: setFilterExcludeFlavours,
  });

  const handleChangeTagFilter = handleChangeFilter({
    includes: filterIncludeTags,
    excludes: filterExcludeTags,
    setIncludes: setFilterIncludeTags,
    setExcludes: setFilterExcludeTags,
  });

  const props = {
    competenceReviewQueueProjects,
    pullRequestReviewQueueProjects,

    competenceReviewQueueLoading: fetchCompetenceReviewQueueLastCall.loading,
    pullRequestReviewQueueLoading: fetchPullRequestQueueLastCall.loading,

    fetchNextCompetenceReviewQueuePage,
    fetchNextPullRequestQueuePage,

    filterIncludeTags,
    filterExcludeTags,

    filterIncludeFlavours,
    filterExcludeFlavours,

    handleChangeFlavourFilter,
    handleChangeTagFilter,
  };
  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    competenceReviewQueueProjectsObject:
      state.apiEntities.competenceReviewQueueProject,
    pullRequestReviewQueueProjectsObject:
      state.apiEntities.pullRequestReviewQueueProject,
    FETCH_COMPETENCE_REVIEW_QUEUE_PAGE:
      state.FETCH_COMPETENCE_REVIEW_QUEUE_PAGE,
    FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE:
      state.FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE,
    teams: state.apiEntities.teams,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchCompetenceReviewQueuePage: ({ page }) => {
      dispatch(
        apiReduxApps.FETCH_COMPETENCE_REVIEW_QUEUE_PAGE.operations.maybeStart({
          data: { page },
        })
      );
    },

    fetchPullRequestReviewQueuePage: ({ page }) => {
      dispatch(
        apiReduxApps.FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE.operations.maybeStart(
          {
            data: { page },
          }
        )
      );
    },

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
  };
};

const GlobalCodeReviewDashboard = connect(
  mapStateToProps,
  mapDispatchToProps
)(GlobalCodeReviewDashboardUnconnected);

export default GlobalCodeReviewDashboard;
