import React, { useEffect, useState } from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";
import { apiReduxApps } from "../../../apiAccess/apiApps";
import { useApiCallbacks } from "../../../hooks";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";

const PAGE_SIZE = 14;

function UserCodeReviewPerformanceUnconnected({
  //   mapStateToProps
  pullRequestReviewsObject,
  competenceReviewsObject,

  FETCH_COMPETENCE_REVIEW_QUALITY_PAGE,
  FETCH_PULL_REQUEST_REVIEW_QUALITY_PAGE,

  // mapDispatchToProps
  fetchCompetenceReviewQualityPage,
  fetchPullRequestQualitiesPage,
}) {
  pullRequestReviewsObject = pullRequestReviewsObject || {};
  competenceReviewsObject = competenceReviewsObject || {};

  const initialEndDate = new Date();
  const initialStartDate = new Date();
  initialStartDate.setDate(initialStartDate.getDate() - PAGE_SIZE);

  const [startDate, setStartDate] = useState(initialStartDate);
  const [endDate, setEndDate] = useState(initialEndDate);

  let urlParams = useParams() || {};
  const user = parseInt(urlParams.userId);

  useEffect(() => {
    fetchCompetenceReviewQualityPage({ page: 1, startDate, endDate, user });
    fetchPullRequestQualitiesPage({ page: 1, startDate, endDate, user });
  }, [startDate, endDate]);

  const competenceReviewQualityPageCall = getLatestMatchingCall({
    callLog: FETCH_COMPETENCE_REVIEW_QUALITY_PAGE,
    requestData: { startDate, endDate },
  });

  useApiCallbacks({
    lastCallEntry: competenceReviewQualityPageCall,
    successResponseCallback: () => {
      if (competenceReviewQualityPageCall.responseData.next) {
        fetchCompetenceReviewQualityPage({
          page: competenceReviewQualityPageCall.requestData.page + 1,
          startDate,
          endDate,
          user,
        });
      }
    },
  });

  const prReviewQualityPageCall = getLatestMatchingCall({
    callLog: FETCH_PULL_REQUEST_REVIEW_QUALITY_PAGE,
    requestData: { startDate, endDate },
  });

  useApiCallbacks({
    lastCallEntry: prReviewQualityPageCall,
    successResponseCallback: () => {
      if (prReviewQualityPageCall.responseData.next) {
        fetchPullRequestQualitiesPage({
          page: prReviewQualityPageCall.requestData.page + 1,
          startDate,
          endDate,
          user,
        });
      }
    },
  });

  function _shiftDates(days) {
    const newStartDate = new Date();
    const newEndDate = new Date();

    newStartDate.setDate(startDate.getDate() + days);
    setStartDate(newStartDate);

    newEndDate.setDate(endDate.getDate() + days);
    setEndDate(newEndDate);
  }

  function handleClickPrevious() {
    _shiftDates(-PAGE_SIZE);
  }

  function handleClickNext() {
    _shiftDates(+PAGE_SIZE);
  }

  const pullRequestReviews = Object.values(pullRequestReviewsObject)
    .filter((o) => new Date(o.submittedAt) <= endDate)
    .filter((o) => new Date(o.submittedAt) >= startDate);
  // TODO: filter by user

  const competenceReviews = Object.values(competenceReviewsObject)
    .filter((o) => new Date(o.timestamp) <= endDate)
    .filter((o) => new Date(o.timestamp) >= startDate);
  // TODO: filter by user

  const props = {
    pullRequestReviews,

    competenceReviews,
    startDate,
    endDate,

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
      dispatch(
        apiReduxApps.FETCH_COMPETENCE_REVIEW_QUALITY_PAGE.operations.maybeStart(
          {
            data: {
              page,
              startDate,
              endDate,
              user,
            },
          }
        )
      );
    },

    fetchPullRequestQualitiesPage: ({ page, startDate, endDate, user }) => {
      dispatch(
        apiReduxApps.FETCH_PULL_REQUEST_REVIEW_QUALITY_PAGE.operations.maybeStart(
          { data: { page, startDate, endDate, user } }
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
