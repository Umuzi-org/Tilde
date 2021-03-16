import React from "react";
import Presentation from "./Presentation";
// import { useParams } from "react-router-dom";
// https://api.github.com/users/sheenarbw/events
import { useParams } from "react-router-dom";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../apiAccess/redux/apiApps";

import { cardDetailsModalOperations } from "../CardDetailsModal/redux";
import { ACTION_NAMES } from "./constants";
import { getLatestMatchingCall } from "../../../utils/ajaxRedux";

// TODO: look nice

const days = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
];

function UserActionsUnconnected({
  authedUserId,
  projectReviews,
  cardSummaries,
  fetchProjectReviewsPages,
  fetchCardCompletions,
  openCardDetailsModal,
  // call logs
  FETCH_RECRUIT_PROJECT_REVIEWS_PAGE,
  FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE,
}) {
  let urlParams = useParams() || {};
  const userId = parseInt(urlParams.userId || authedUserId || 0);

  React.useEffect(() => {
    fetchProjectReviewsPages({
      dataSequence: [
        { page: 1, reviewerUser: userId },
        // { page: 1, recruitUsers: [userId] },
      ],
    });
  }, [fetchProjectReviewsPages, userId]);

  React.useEffect(() => {
    fetchCardCompletions({ page: 1, assigneeUserId: userId });
  }, [fetchCardCompletions, userId]);

  const latestProjectReviewsCall = getLatestMatchingCall({
    callLog: FETCH_RECRUIT_PROJECT_REVIEWS_PAGE,
    requestData: { reviewerUser: userId },
  }) || { loading: true };

  const lastCompletedCardsPage = getLatestMatchingCall({
    callLog: FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE,
    reviewerUser: { assigneeUserId: userId },
  }) || { loading: true };

  const handleClickOpenProjectDetails = ({ cardId }) => {
    openCardDetailsModal({ cardId });
  };

  const anyLoading =
    latestProjectReviewsCall.loading || lastCompletedCardsPage.loading;

  const fetchNextPages = () => {
    if (anyLoading) return;
    if (latestProjectReviewsCall.responseData.results.length > 0) {
      const nextReviewPage = latestProjectReviewsCall.requestData.page + 1;
      fetchProjectReviewsPages({
        dataSequence: [{ page: nextReviewPage, reviewerUser: userId }],
      });
    }
    if (lastCompletedCardsPage.responseData.results.length > 0) {
      const nextCardPage = lastCompletedCardsPage.requestData.page + 1;
      fetchCardCompletions({ page: nextCardPage, assigneeUserId: userId });
    }
  };

  function handleScroll(e) {
    const atBottom =
      e.target.scrollTop + e.target.clientHeight === e.target.scrollHeight;

    if (atBottom) {
      fetchNextPages();
    }
  }

  const getTimeFields = (date) => {
    if (!date) {
      console.log("date is falsy!!!!!!!!!!!!!");
      return {};
    }

    const timestamp = new Date(date);
    const dateStr =
      days[timestamp.getDay()] + " " + timestamp.toLocaleDateString();

    return {
      timestamp,
      dateStr,
    };
  };

  const completedCards = Object.values(cardSummaries)
    .filter((card) => card.assignees.indexOf(userId) !== -1)
    .map((card) => {
      const timeFields = getTimeFields(card.completeTime);

      return {
        ...card,
        ...timeFields,

        actionType: ACTION_NAMES.CARD_COMPLETED,
      };
    });

  const reviewsDone = Object.values(projectReviews)
    .filter((review) => review.reviewerUser === userId)
    .map((review) => {
      const timeFields = getTimeFields(review.timestamp);
      return {
        ...review,
        ...timeFields,
        actionType: ACTION_NAMES.COMPETENCE_REVIEW_DONE,
      };
    });

  let actionLog = [...reviewsDone, ...completedCards].filter((o) => o.dateStr);

  actionLog.sort((action1, action2) => action2.timestamp - action1.timestamp);

  let orderedDates = [];

  let actionLogByDate = {};
  actionLog.forEach((o) => {
    const date = o.dateStr;
    if (orderedDates.indexOf(date) === -1) orderedDates.push(date);
    actionLogByDate[date] = actionLogByDate[date] || [];
    actionLogByDate[date].push(o);
  });

  const props = {
    orderedDates,
    actionLogByDate,
    anyLoading,
    handleClickOpenProjectDetails,
    handleScroll,
  };
  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    users: state.Entities.users || {},
    projectReviews: state.Entities.projectReviews || {},
    cardSummaries: state.Entities.projectSummaryCards || {},
    authedUserId: state.App.authUser.userId,
    FETCH_RECRUIT_PROJECT_REVIEWS_PAGE:
      state.FETCH_RECRUIT_PROJECT_REVIEWS_PAGE,
    FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE:
      state.FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchProjectReviewsPages: ({ dataSequence }) => {
      dispatch(
        apiReduxApps.FETCH_RECRUIT_PROJECT_REVIEWS_PAGE.operations.startCallSequence(
          { dataSequence }
        )
      );
    },

    fetchCardCompletions: ({ assigneeUserId, page }) => {
      dispatch(
        apiReduxApps.FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE.operations.start({
          data: { assigneeUserId, page },
        })
      );
    },

    fetchUser: ({ userId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_USER.operations.maybeStart({
          data: { userId },
        })
      );
    },

    openCardDetailsModal: ({ cardId }) => {
      dispatch(cardDetailsModalOperations.openCardDetailsModal({ cardId }));
    },
  };
};

const UserActions = connect(
  mapStateToProps,
  mapDispatchToProps
)(UserActionsUnconnected);

export default UserActions;
