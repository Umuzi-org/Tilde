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
const matchEventTypesWithColors = ({ eventTypes, eventTypeColors }) => {
  const arr = [];
  eventTypes = Object.keys(eventTypes).map((key) => eventTypes[key]);

  eventTypes.forEach((eventType) => {
    arr.push({
      id: eventType.id,
      eventName: eventType.name,
      eventColor: eventTypeColors[eventType.name],
    });
  });
  return arr;
};

function mapData({ eventTypesWithColors, activityLogEntries }) {
  activityLogEntries = Object.keys(activityLogEntries).map(
    (key) => activityLogEntries[key]
  );

  const newData = activityLogEntries.map((item, index) => {
    const data = eventTypesWithColors.find(
      (elem) => elem.id === item.eventType
    );
    return {
      ...item,
      eventName: data ? data.eventName : "",
      eventColor: data ? data.eventColor : "",
    };
  });
  return newData;
}

function UserActionsUnconnected({
  authedUserId,
  projectReviews,
  cardSummaries,
  fetchProjectReviewsPages,
  fetchCardCompletions,
  userBurndownStats,
  fetchUserBurndownStats,
  fetchEventTypes,
  // call logs
  FETCH_RECRUIT_PROJECT_REVIEWS_PAGE,
  FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE,
  eventTypes,
  activityLogEntries,
  fetchActivityLogEntries,
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
    fetchActivityLogEntries({
      actorUser: userId,
      page: 1,
    });
  }, [fetchActivityLogEntries, userId]);

  useEffect(() => {
    fetchEventTypes({
      page: 1,
    });
  }, [fetchEventTypes]);

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

  // const latestEventTypesPage = getLatestMatchingCall({
  //   callLog: FETCH_EVENT_TYPES,
  //   requestData: { page: 1 },
  // });

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
  let orderedDates2 = [];

  Object.keys(activityLogEntries).map((o) => {
    const date = activityLogEntries[o].timestamp;
    orderedDates2.push(date);
  });
  orderedDates2 = [...new Set(orderedDates2)];

  let actionLogByDate = {};
  actionLog.forEach((o) => {
    const date = o.dateStr;
    if (orderedDates.indexOf(date) === -1) orderedDates.push(date);
    actionLogByDate[date] = actionLogByDate[date] || [];
    actionLogByDate[date].push(o);
  });

  const eventTypesWithColors = matchEventTypesWithColors({
    eventTypes,
    eventTypeColors,
  });

  activityLogEntries = mapData({ eventTypesWithColors, activityLogEntries });

  function compare(activityLogEntries, actionLogByDate) {
    const actions = Object.values(actionLogByDate);
    let newData;
    console.log(actionLogByDate);
    actions.map((action) => {
      newData = activityLogEntries.map((item, index) => {
        const data = action.find(
          (elem) =>
            elem.timestamp.toString() !==
            new Date(item.timestamp.toString()).toString()
        );

        const obj = {
          ...item,
          cardName: data ? data.title : "",
        };

        return obj;
      });
    });
    return newData;
  }

  activityLogEntries = compare(activityLogEntries, actionLogByDate);

  const props = {
    orderedDates,
    orderedDates2,
    actionLogByDate,
    eventTypes,
    activityLogEntries,
    anyLoading,
    handleScroll,
    currentUserBurndownStats,
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
    activityLogEntries: state.apiEntities.activityLogEntries,
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
    fetchActivityLogEntries: ({ actorUser, page }) => {
      dispatch(
        apiReduxApps.FETCH_ACTIVITY_LOG_ENTRIES.operations.start({
          data: { actorUser, page },
        })
      );
    },
    fetchEventTypes: ({ page }) => {
      dispatch(
        apiReduxApps.FETCH_EVENT_TYPES.operations.start({
          data: { page },
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
