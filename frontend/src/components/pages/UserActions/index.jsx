import React, { useEffect } from "react";
import Presentation from "./Presentation";
// import { useParams } from "react-router-dom";
// https://api.github.com/users/sheenarbw/events
import { useParams } from "react-router-dom";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../apiAccess/apiApps";

import { ACTION_NAMES } from "./constants";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";
import Loading from "../../widgets/Loading";
import { eventTypeColors } from "../../../colors";

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
  userBurndownStats,
  fetchUserBurndownStats,
  eventTypes,
  fetchEventTypes,
  activityLogDayCounts,
  fetchActivityLogDayCountsPage,
  // call logs
  FETCH_RECRUIT_PROJECT_REVIEWS_PAGE,
  FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE,
}) {
  let urlParams = useParams() || {};
  const userId = parseInt(urlParams.userId || authedUserId || 0);
  const currentUserBurndownStats = Object.values(userBurndownStats).filter(
    (snapshot) => snapshot.user === userId
  );

  useEffect(() => {
    fetchProjectReviewsPages({
      dataSequence: [
        { page: 1, reviewerUser: userId },
        // { page: 1, recruitUsers: [userId] },
      ],
    });
  }, [fetchProjectReviewsPages, userId]);

  useEffect(() => {
    fetchCardCompletions({ page: 1, assigneeUserId: userId });
    fetchUserBurndownStats({ userId });
  }, [fetchCardCompletions, fetchUserBurndownStats, userId]);

  useEffect(() => {
    fetchEventTypes({ page: 1 });
  }, [fetchEventTypes]);

  useEffect(() => {
    fetchActivityLogDayCountsPage({ actorUser: userId, page: 1 });
  }, [fetchActivityLogDayCountsPage, userId]);

  if (
    !userId ||
    !fetchProjectReviewsPages ||
    !fetchCardCompletions ||
    !fetchUserBurndownStats
  )
    return <Loading />;

  const latestProjectReviewsCall = getLatestMatchingCall({
    callLog: FETCH_RECRUIT_PROJECT_REVIEWS_PAGE,
    requestData: { reviewerUser: userId },
  }) || { loading: true };

  const lastCompletedCardsPage = getLatestMatchingCall({
    callLog: FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE,
    requestData: { assigneeUserId: userId },
  }) || { loading: true };

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
      e.target.scrollTop + e.target.clientHeight >= e.target.scrollHeight;

    if (atBottom) {
      fetchNextPages();
    }
  }

  const getTimeFields = (date) => {
    if (!date) {
      console.warn("date is falsy!!!!!!!!!!!!!");
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
  if (!cardSummaries) return <Loading />;
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
  if (!projectReviews) return <Loading />;
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

  const matchColorsToEventTypes = () => {
    const eventTypeNames = [];

    for (const eventName in eventTypes) {
      eventTypeNames.push(eventTypes[eventName].name);
    }

    const colors = [...Object.values(eventTypeColors)];
    const sortedEventTypeNames = eventTypeNames.sort();
    const evenTypeColorKeys = [...Object.keys(eventTypeColors)].sort();

    for (let i = 0; i < eventTypes.length; i++) {
      if (sortedEventTypeNames[i] === evenTypeColorKeys[i]) {
        eventTypes[i].color = colors[i];
      }
    }
  };

  matchColorsToEventTypes();

  console.log(activityLogDayCounts);

  const props = {
    orderedDates,
    actionLogByDate,
    anyLoading,
    handleScroll,
    currentUserBurndownStats,
    activityLogDayCounts,
  };
  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    projectReviews: state.apiEntities.projectReviews,
    cardSummaries: state.apiEntities.projectSummaryCards,
    authedUserId: state.App.authUser.userId,
    FETCH_RECRUIT_PROJECT_REVIEWS_PAGE:
      state.FETCH_RECRUIT_PROJECT_REVIEWS_PAGE,
    FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE:
      state.FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE,
    userBurndownStats: state.apiEntities.burndownSnapshots || {},
    eventTypes: state.apiEntities.eventTypes,
    activityLogDayCounts: state.apiEntities.activityLogDayCounts,
    FETCH_EVENT_TYPES: state.FETCH_EVENT_TYPES,
    FETCH_ACTIVITY_LOG_DAY_COUNTS_PAGE:
      state.FETCH_ACTIVITY_LOG_DAY_COUNTS_PAGE,
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
    //TODO Implement Page check
    fetchUserBurndownStats: ({ userId }) => {
      dispatch(
        apiReduxApps.FETCH_USER_BURNDOWN_SNAPSHOTS_PAGE.operations.maybeStart({
          data: {
            userId: parseInt(userId),
            page: 1,
          },
        })
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
          data: { userId: parseInt(userId) },
        })
      );
    },

    fetchEventTypes: ({ page }) => {
      dispatch(
        apiReduxApps.FETCH_EVENT_TYPES.operations.maybeStart({
          data: { page },
        })
      );
    },

    fetchActivityLogDayCountsPage: ({ actorUser, page }) => {
      dispatch(
        apiReduxApps.FETCH_ACTIVITY_LOG_DAY_COUNTS_PAGE.operations.maybeStart({
          data: { actorUser, page },
        })
      );
    },
  };
};

const UserActions = connect(
  mapStateToProps,
  mapDispatchToProps
)(UserActionsUnconnected);

export default UserActions;
