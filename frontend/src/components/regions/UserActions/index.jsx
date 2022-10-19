import React, { useEffect } from "react";
import Presentation from "./Presentation";
// import { useParams } from "react-router-dom";
// https://api.github.com/users/sheenarbw/events
import { useParams } from "react-router-dom";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../apiAccess/apiApps";

import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";
import Loading from "../../widgets/Loading";
import { eventTypeColors } from "../../../colors";
import { addEventColorsToLogEntries } from "./utils.js";

function UserActionsUnconnected({
  authedUserId,
  fetchCardCompletions,
  userBurndownStats,
  fetchUserBurndownStats,
  fetchActivityLogEntries,
  fetchEventTypes,
  eventTypes,
  activityLogEntries,
  // call logs
  FETCH_ACTIVITY_LOG_ENTRIES,
}) {
  let urlParams = useParams() || {};
  const userId = parseInt(urlParams.userId || authedUserId || 0);
  userBurndownStats = userBurndownStats || {};
  const currentUserBurndownStats = Object.values(userBurndownStats).filter(
    (snapshot) => snapshot.user === userId
  );

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
  if (!userId || !fetchUserBurndownStats) return <Loading />;
  if (!activityLogEntries) return <Loading />;

  const latestActivityLogPage = getLatestMatchingCall({
    callLog: FETCH_ACTIVITY_LOG_ENTRIES,
    requestData: { actorUser: userId },
  }) || { loading: true };

  const anyLoading = latestActivityLogPage.loading;

  const fetchNextPages = () => {
    if (anyLoading) return;
    if (latestActivityLogPage.responseData.results.length > 0) {
      const nextCardPage = latestActivityLogPage.requestData.page + 1;
      fetchActivityLogEntries({ page: nextCardPage, actorUser: userId });
    }
  };

  function handleScroll(e) {
    const atBottom =
      e.target.scrollTop + e.target.clientHeight >= e.target.scrollHeight;

    if (atBottom) {
      fetchNextPages();
    }
  }

  let orderedDates = [];

  Object.keys(activityLogEntries).map((o) => {
    const date = activityLogEntries[o].timestamp;
    orderedDates.push(date.substring(0, 10));
    return orderedDates.sort((time1, time2) => {
      return new Date(time1) < new Date(time2) ? 1 : -1;
    });
  });

  orderedDates = [...new Set(orderedDates)];

  activityLogEntries = addEventColorsToLogEntries({
    eventTypes,
    eventTypeColors,
    activityLogEntries,
  });

  const props = {
    orderedDates,
    anyLoading,
    handleScroll,
    currentUserBurndownStats,
    activityLogEntries,
    fetchNextPages,
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
    FETCH_ACTIVITY_LOG_ENTRIES: state.FETCH_ACTIVITY_LOG_ENTRIES,
    userBurndownStats: state.apiEntities.burndownSnapshots,
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
