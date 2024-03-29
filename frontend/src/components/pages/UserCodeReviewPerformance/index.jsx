import React, { useEffect, useState } from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";
import { apiReduxApps } from "../../../apiAccess/apiApps";
// import { useApiCallbacks } from "../../../hooks";
// import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";

import { apiUtilitiesOperations } from "../../../apiAccess/redux";

const PAGE_SIZE = 7;

export function UserCodeReviewPerformanceUnconnected({
  //   mapStateToProps
  pullRequestReviewsObject,
  competenceReviewsObject,

  // FETCH_COMPETENCE_REVIEW_QUALITY_PAGE,    // TODO: show loading spinners or progress bars
  // FETCH_PULL_REQUEST_REVIEW_QUALITY_PAGE,

  // mapDispatchToProps
  fetchCompetenceReviewQualityPage,
  fetchPullRequestQualitiesPage,

  // storybook
  forceUser,
  forceToday,
}) {
  pullRequestReviewsObject = pullRequestReviewsObject || {};
  competenceReviewsObject = competenceReviewsObject || {};

  const [datePageOffset, setDatePageOffset] = useState(0);
  const [showReviewHelpModal, setShowReviewHelpModal] = useState(false);

  const startDate = forceToday ? new Date(Date.parse(forceToday)) : new Date();
  const endDate = forceToday ? new Date(Date.parse(forceToday)) : new Date();

  startDate.setDate(startDate.getDate() - (1 + datePageOffset) * PAGE_SIZE);
  endDate.setDate(endDate.getDate() - datePageOffset * PAGE_SIZE);

  let urlParams = useParams() || {};
  const user = forceUser || parseInt(urlParams.userId);

  useEffect(() => {
    fetchCompetenceReviewQualityPage({ page: 1, startDate, endDate, user });
    fetchPullRequestQualitiesPage({ page: 1, startDate, endDate, user });
    // NOTE: that if se add startDate and endDate to the deps then we get into an infinite loop
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [datePageOffset, user]);

  function handleClickPrevious() {
    setDatePageOffset(datePageOffset + 1);
  }

  function handleClickNext() {
    setDatePageOffset(Math.max(datePageOffset - 1, 0));
  }

  function handleOpenReviewHelpModal() {
    setShowReviewHelpModal(true);
  }
  function handleCloseReviewHelpModal() {
    setShowReviewHelpModal(false);
  }

  const pullRequestReviews = Object.values(pullRequestReviewsObject)
    .filter((o) => new Date(o.submittedAt) <= endDate)
    .filter((o) => new Date(o.submittedAt) >= startDate)
    .filter((o) => o.user === user);

  const competenceReviews = Object.values(competenceReviewsObject)
    .filter((o) => new Date(o.timestamp) <= endDate)
    .filter((o) => new Date(o.timestamp) >= startDate)
    .filter((o) => o.reviewerUser === user);

  const props = {
    pullRequestReviews,
    competenceReviews,

    startDate,
    endDate,
    days: PAGE_SIZE,

    showReviewHelpModal,
    handleOpenReviewHelpModal,
    handleCloseReviewHelpModal,

    handleClickPrevious,
    handleClickNext,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    FETCH_COMPETENCE_REVIEW_QUALITY_PAGE:
      state.FETCH_COMPETENCE_REVIEW_QUALITY_PAGE,
    FETCH_PULL_REQUEST_REVIEW_QUALITY_PAGE:
      state.FETCH_PULL_REQUEST_REVIEW_QUALITY_PAGE,

    pullRequestReviewsObject: state.apiEntities.pullRequestReviewQualities,
    competenceReviewsObject: state.apiEntities.competenceReviewQualities,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchCompetenceReviewQualityPage: ({ page, startDate, endDate, user }) => {
      const data = {
        page,
        startDate,
        endDate,
        user,
      };
      dispatch(
        apiReduxApps.FETCH_COMPETENCE_REVIEW_QUALITY_PAGE.operations.maybeStart(
          {
            data,
            successDispatchActions: [
              apiUtilitiesOperations.fetchAllPages({
                API_BASE_TYPE: "FETCH_COMPETENCE_REVIEW_QUALITY_PAGE",
                requestData: data,
              }),
            ],
          }
        )
      );
    },

    fetchPullRequestQualitiesPage: ({ page, startDate, endDate, user }) => {
      const data = { page, startDate, endDate, user };
      dispatch(
        apiReduxApps.FETCH_PULL_REQUEST_REVIEW_QUALITY_PAGE.operations.maybeStart(
          {
            data,
            successDispatchActions: [
              apiUtilitiesOperations.fetchAllPages({
                API_BASE_TYPE: "FETCH_PULL_REQUEST_REVIEW_QUALITY_PAGE",
                requestData: data,
              }),
            ],
          }
        )
      );
    },
  };
};
const UserCodeReviewPerformance = connect(
  mapStateToProps,
  mapDispatchToProps
)(UserCodeReviewPerformanceUnconnected);
export default UserCodeReviewPerformance;
