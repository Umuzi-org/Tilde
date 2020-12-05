import React, { useEffect } from "react";
import Presentation from "./Presentation";

import { apiReduxApps } from "../../../apiAccess/redux/apiApps";
import { connect } from "react-redux";

import consts, { READY } from "../../../constants";

import { useParams } from "react-router-dom";

const maxStartIndex = 5;

function boardFromCards({ cards }) {
  return Object.keys(consts.AGILE_COLUMNS).map((columnName) => {
    return {
      label: columnName,
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

function getLatestMatchingCall({
  fetchCardsCallLog,
  status,
  assigneeUserId,
  reviewerUserId,
}) {
  return fetchCardsCallLog.reverse().find((logEntry) => {
    if (logEntry.requestData.status !== status) return false;

    if (
      (assigneeUserId !== undefined) &
      (logEntry.requestData.assigneeUserId !== assigneeUserId)
    )
      return false;
    if (
      (reviewerUserId !== undefined) &
      (logEntry.requestData.reviewerUserId !== reviewerUserId)
    )
      return false;
    return true;
  });
}

export function getLatestCallNextPageValue({
  fetchCardsCallLog,
  status,
  assigneeUserId,
  reviewerUserId,
}) {
  const lastCall = getLatestMatchingCall({
    fetchCardsCallLog,
    status,
    assigneeUserId,
    reviewerUserId,
  });

  if (lastCall === undefined) return null;
  if (lastCall === null) return null;
  if (lastCall.responseData === null) return null;
  const nextUrl = lastCall.responseData.next;
  if (nextUrl) {
    var url = new URL(nextUrl);
    const nextPageNumber = url.searchParams.get("page");
    return parseInt(nextPageNumber);
  }
  return null;
}

function AgileBoardUnconnected({
  cards,
  fetchCardPages,
  fetchCardsCallLog,
  authedUserId,
  fetchInitialCards,
}) {
  let urlParams = useParams() || {};
  const userId = parseInt(urlParams.userId || authedUserId || 0);

  useEffect(() => {
    fetchInitialCards({ userId });
  }, [fetchInitialCards, userId]);

  const filteredCards = filterCardsByUserId({
    cards,
    userId,
  });

  function fetchNextColumnPage(columnLabel) {
    const statuses = consts.AGILE_COLUMNS[columnLabel];

    let callSequenceData = [];

    for (let status of statuses) {
      let assignedPageNumber = getLatestCallNextPageValue({
        fetchCardsCallLog,
        status,
        assigneeUserId: userId,
      });

      if (assignedPageNumber !== null) {
        callSequenceData.push({
          page: assignedPageNumber,
          status,
          assigneeUserId: userId,
        });
      }

      let reviewPageNumber = getLatestCallNextPageValue({
        fetchCardsCallLog,
        status,
        reviewerUserId: userId,
      });
      if (reviewPageNumber !== null) {
        callSequenceData.push({
          page: reviewPageNumber,
          status,
          reviewerUserId: userId,
        });
      }
    }

    fetchCardPages({ dataSequence: callSequenceData });
  }

  function handleColumnScroll({ column }) {
    function eventHandler(e) {
      const atBottom =
        e.target.scrollTop + e.target.clientHeight === e.target.scrollHeight;

      if (atBottom) {
        //   console.log("At bottom")
        fetchNextColumnPage(column.label);
      }
    }
    return eventHandler;
  }

  const canStart = ({ card, index }) => {
    if (card.status !== READY) return false;
    return index <= maxStartIndex;
    // # TODO: check number of work in progress issues
  };
  let props = {
    userId,
    cards: filteredCards,
    board: boardFromCards({ cards: filteredCards }),

    handleColumnScroll,
    canStart,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    cards: state.Entities.cards || {},
    fetchCardsCallLog: state.FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
    authedUserId: state.App.authUser.userId,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchCardPages: ({ dataSequence }) => {
      dispatch(
        apiReduxApps.FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE.operations.startCallSequence(
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

      const dataSequence = [dataSequence1, dataSequence2].flat();

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
