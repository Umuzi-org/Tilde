import React, { useEffect } from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";

import { apiReduxApps } from "../../../apiAccess/apiApps";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";

function GlobalCodeReviewDashboardUnconnected({
  // mapStateToProps

  competenceReviewQueueProjectsObject,
  pullRequestReviewQueueProjectsObject,
  FETCH_COMPETENCE_REVIEW_QUEUE_PAGE,
  FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE,

  // mapDispatchToProps

  fetchCompetenceReviewQueuePage,
  fetchPullRequestReviewQueuePage,
}) {
  useEffect(() => {
    fetchCompetenceReviewQueuePage({ page: 1 });
    fetchPullRequestReviewQueuePage({ page: 1 });
  }, [fetchCompetenceReviewQueuePage, fetchPullRequestReviewQueuePage]);

  const fetchCompetenceReviewQueueLastCall = getLatestMatchingCall({
    callLog: FETCH_COMPETENCE_REVIEW_QUEUE_PAGE,
  }) || { loading: true };
  const fetchPullRequestQueueLastCall = getLatestMatchingCall({
    callLog: FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE,
  }) || { loading: true };

  console.log({
    fetchPullRequestQueueLastCall,
    fetchCompetenceReviewQueueLastCall,
  });

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

  const props = {
    competenceReviewQueueProjects,
    pullRequestReviewQueueProjects,

    competenceReviewQueueLoading: fetchCompetenceReviewQueueLastCall.loading,
    pullRequestReviewQueueLoading: fetchPullRequestQueueLastCall.loading,

    fetchNextCompetenceReviewQueuePage,
    fetchNextPullRequestQueuePage,
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
  };
};

const GlobalCodeReviewDashboard = connect(
  mapStateToProps,
  mapDispatchToProps
)(GlobalCodeReviewDashboardUnconnected);

export default GlobalCodeReviewDashboard;
