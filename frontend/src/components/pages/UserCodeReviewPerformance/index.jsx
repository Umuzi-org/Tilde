import React, { useEffect, useState } from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";
import { apiReduxApps } from "../../../apiAccess/apiApps";
// import { useApiCallbacks } from "../../../hooks";
// import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";

import { apiUtilitiesOperations } from "../../../apiAccess/redux";

const PAGE_SIZE = 7;

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

  const [datePageOffset, setDatePageOffset] = useState(0);

  const startDate = new Date();
  const endDate = new Date();

  startDate.setDate(startDate.getDate() - (1 + datePageOffset) * PAGE_SIZE);
  endDate.setDate(endDate.getDate() - datePageOffset * PAGE_SIZE);

  let urlParams = useParams() || {};
  const user = parseInt(urlParams.userId);

  useEffect(() => {
    fetchCompetenceReviewQualityPage({ page: 1, startDate, endDate, user });
    fetchPullRequestQualitiesPage({ page: 1, startDate, endDate, user });
  }, [datePageOffset]);

  //   const competenceReviewQualityPageCall = getLatestMatchingCall({
  //     callLog: FETCH_COMPETENCE_REVIEW_QUALITY_PAGE,
  //     requestData: { startDate, endDate },
  //   });

  //   useApiCallbacks({
  //     lastCallEntry: competenceReviewQualityPageCall,
  //     successResponseCallback: () => {
  //       if (competenceReviewQualityPageCall.responseData.next) {
  //         fetchCompetenceReviewQualityPage({
  //           page: competenceReviewQualityPageCall.requestData.page + 1,
  //           startDate,
  //           endDate,
  //           user,
  //         });
  //       }
  //     },
  //   });

  //   const prReviewQualityPageCall = getLatestMatchingCall({
  //     callLog: FETCH_PULL_REQUEST_REVIEW_QUALITY_PAGE,
  //     requestData: { startDate, endDate },
  //   });

  //   useApiCallbacks({
  //     lastCallEntry: prReviewQualityPageCall,
  //     successResponseCallback: () => {
  //       if (prReviewQualityPageCall.responseData.next) {
  //         fetchPullRequestQualitiesPage({
  //           page: prReviewQualityPageCall.requestData.page + 1,
  //           startDate,
  //           endDate,
  //           user,
  //         });
  //       }
  //     },
  //   });

  function handleClickPrevious() {
    setDatePageOffset(datePageOffset + 1);
  }

  function handleClickNext() {
    setDatePageOffset(Math.max(datePageOffset - 1, 0));
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
