import React, { useEffect } from "react";
import Presentation from "./Presentation";
import { apiReduxApps } from "../../../apiAccess/apiApps";
import { connect } from "react-redux";
import consts from "../../../constants";
import { useParams } from "react-router-dom";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";
import Loading from "../../widgets/Loading";

export function boardFromCards({ cards, latestCalls }) {
  return Object.keys(consts.AGILE_COLUMNS).map((columnName) => {
    return {
      label: columnName,
      totalCards: Object.keys(latestCalls)
        .filter(
          (status) => consts.AGILE_COLUMNS[columnName].indexOf(status) !== -1
        )
        .map((status) => latestCalls[status].totalCards)
        .reduce((a, b) => a + b),
      cards: Object.values(cards)
        .filter(
          (card) => consts.AGILE_COLUMNS[columnName].indexOf(card.status) !== -1
        )
        .map((card) => card.id)
        .sort((card) => card.order),
    };
  });
}

function filterCardsByUserId({ cards, userId }) {
  let filteredCards = {};

  for (let cardId in cards) {
    if (cards[cardId].assignees.indexOf(userId) !== -1) {
      filteredCards[cardId] = cards[cardId];
    } else if (cards[cardId].reviewers.indexOf(userId) !== -1) {
      filteredCards[cardId] = cards[cardId];
    }
  }
  return filteredCards;
}

function getAllLatestCalls({
  FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
  userId,
}) {
  let result = {};

  const defaultCallLogEntry = {
    loading: true,
    requestData: { page: 0 },
    responseData: { count: -1 },
  };

  for (let status in consts.AGILE_CARD_STATUS_CHOICES) {
    let current = {
      anyLoading: false,
      lastAssigneeCallPage: 0,
      lastReviewerCallPage: 0,
      assigneeCallResponseCount: -1,
      reviewerCallResponseCount: -1,
      totalCards: 0,
    };

    const lastAssigneeCall =
      getLatestMatchingCall({
        callLog: FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
        requestData: {
          assigneeUserId: userId,
          status,
        },
      }) || defaultCallLogEntry;

    current.anyLoading = current.anyLoading || lastAssigneeCall.loading;
    current.lastAssigneeCallPage = lastAssigneeCall.requestData.page;
    current.assigneeCallResponseCount =
      lastAssigneeCall.responseData && lastAssigneeCall.responseData.results
        ? lastAssigneeCall.responseData.results.length
        : -1;

    let totalCards = lastAssigneeCall.responseData
      ? lastAssigneeCall.responseData.count
      : 0;

    if (consts.AGILE_CARD_STATUS_CHOICES_SHOW_REVIEWER.includes(status)) {
      const lastReviewerCall =
        getLatestMatchingCall({
          callLog: FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
          requestData: {
            reviewerUserId: userId,
            status,
          },
        }) || defaultCallLogEntry;

      totalCards = totalCards + lastReviewerCall.responseData?.count;

      current.anyLoading = current.anyLoading || lastReviewerCall.loading;
      current.lastReviewerCallPage = lastReviewerCall.requestData.page;
      current.reviewerCallResponseCount =
        lastReviewerCall.responseData && lastReviewerCall.responseData.results
          ? lastReviewerCall.responseData.results.length
          : -1;
    }
    current.totalCards = totalCards;
    result[status] = { ...current };
  }
  return result;
}

/*
Given a bunch of info from getAllLatestCalls, return a
list of column titles which should contain loading spinners */
function getColumnsLoading({ latestCallStates }) {
  const result = Object.keys(consts.AGILE_COLUMNS).filter((columnName) => {
    for (let status of consts.AGILE_COLUMNS[columnName]) {
      if (latestCallStates[status].anyLoading) return true;
    }
    return undefined;
  });

  return result;
}

function AgileBoardUnconnected({
  cards,
  users,
  fetchCardPages,
  FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
  authedUserId,
  fetchInitialCards,
}) {
  let urlParams = useParams() || {};
  const userId = parseInt(urlParams.userId || authedUserId || 0);

  useEffect(() => {
    if (userId !== undefined) fetchInitialCards({ userId });
  }, [fetchInitialCards, userId]);

  const filteredCards = filterCardsByUserId({
    cards,
    userId,
  });

  const latestCallStates =
    userId !== undefined
      ? getAllLatestCalls({
          FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
          userId,
        })
      : {};

  function fetchNextColumnPage({ columnLabel, latestCallStates }) {
    const statuses = consts.AGILE_COLUMNS[columnLabel];
    for (let status of statuses) {
      // we are still fetching the last bunch. Nothing to do
      if (latestCallStates[status].anyLoading) return;
    }

    let dataSequence = [];

    for (let status of statuses) {
      if (latestCallStates[status].assigneeCallResponseCount > 0)
        dataSequence.push({
          assigneeUserId: userId,
          page: latestCallStates[status].lastAssigneeCallPage + 1,
          status,
        });

      if (consts.AGILE_CARD_STATUS_CHOICES_SHOW_REVIEWER.includes(status)) {
        // we need to also fetch the next review page
        if (latestCallStates[status].reviewerCallResponseCount > 0)
          dataSequence.push({
            reviewerUserId: userId,
            page: latestCallStates[status].lastReviewerCallPage + 1,
            status,
          });
      }
    }

    if (dataSequence.length > 0) fetchCardPages({ dataSequence });
  }

  const columnsLoading = getColumnsLoading({ latestCallStates });

  function handleColumnScroll({ column }) {
    if (columnsLoading.includes(column.label)) return () => {};

    function eventHandler(e) {
      const atBottom =
        e.target.scrollTop + e.target.clientHeight >= e.target.scrollHeight;

      if (atBottom) {
        fetchNextColumnPage({ columnLabel: column.label, latestCallStates });
      }
    }
    return eventHandler;
  }

  const viewedUser = users[userId];
  if (!viewedUser) {
    return <Loading />;
  }

  let props = {
    userId,
    cards: filteredCards,
    board: boardFromCards({
      cards: filteredCards,
      latestCalls: latestCallStates,
    }),
    columnsLoading,
    viewedUser: users[userId],

    handleColumnScroll,
  };
  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    users: state.apiEntities.users || {},
    cards: state.apiEntities.cards || {},
    FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE:
      state.FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
    authedUserId: state.App.authUser.userId,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchCardPages: ({ dataSequence }) => {
      dispatch(
        apiReduxApps.FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE.operations.maybeStartCallSequence(
          { dataSequence }
        )
      );
    },

    fetchInitialCards: ({ userId }) => {
      const dataSequence1 = Object.keys(consts.AGILE_CARD_STATUS_CHOICES).map(
        (status) => {
          return {
            page: 1,
            assigneeUserId: userId,
            status,
          };
        }
      );
      const dataSequence2 = consts.AGILE_CARD_STATUS_CHOICES_SHOW_REVIEWER.map(
        (status) => {
          return {
            page: 1,
            reviewerUserId: userId,
            status,
          };
        }
      );

      const dataSequence3 = [
        // TODO: these items should not be necessary. See issue #145
        { page: 2, assigneeUserId: userId, status: consts.READY },
        { page: 2, assigneeUserId: userId, status: consts.BLOCKED },
      ];

      const dataSequence = [dataSequence1, dataSequence2, dataSequence3].flat();

      dispatch(
        apiReduxApps.FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE.operations.maybeStartCallSequence(
          { dataSequence }
        )
      );
    },
  };
};

const AgileBoard = connect(
  mapStateToProps,
  mapDispatchToProps
)(AgileBoardUnconnected);

export default AgileBoard;
