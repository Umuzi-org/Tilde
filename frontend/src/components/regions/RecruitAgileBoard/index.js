import React from "react";
import Presentation from "./Presentation";

import { apiReduxApps } from "../../../apiAccess/redux/apiApps";
import { connect } from "react-redux";

import consts, { READY } from "../../../constants";

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
  AppFilter,
  fetchCardPages,
  fetchCardsCallLog,
}) {
  function fetchNextColumnPage(columnLabel) {
    const statuses = consts.AGILE_COLUMNS[columnLabel];

    let callSequenceData = [];

    for (let status of statuses) {
      let assignedPageNumber = getLatestCallNextPageValue({
        fetchCardsCallLog,
        status,
        assigneeUserId: AppFilter.userId,
      });

      if (assignedPageNumber !== null) {
        callSequenceData.push({
          page: assignedPageNumber,
          status,
          assigneeUserId: AppFilter.userId,
        });
      }

      let reviewPageNumber = getLatestCallNextPageValue({
        fetchCardsCallLog,
        status,
        reviewerUserId: AppFilter.userId,
      });
      if (reviewPageNumber !== null) {
        callSequenceData.push({
          page: reviewPageNumber,
          status,
          reviewerUserId: AppFilter.userId,
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
        fetchNextColumnPage(column.label);
      }
    }
    return eventHandler;
  }

  const filteredCards = filterCardsByUserId({
    cards,
    userId: AppFilter.userId,
  });

  let props = {
    cards: filteredCards,
    board: boardFromCards({ cards: filteredCards }),
  };

  const canStart = ({ card, index }) => {
    if (card.status !== READY) return false;
    return index <= maxStartIndex;
    // # TODO: check number of work in progress issues
  };

  return (
    <Presentation
      {...props}
      handleColumnScroll={handleColumnScroll}
      canStart={canStart}
    />
  );
}

const mapStateToProps = (state) => {
  return {
    AppFilter: state.AppFilter,
    cards: state.Entities.cards || {},
    fetchCardsCallLog: state.FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
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
    // fetchAgileCardsPageStart: ({ page, status, assigneeUserId }) => {
    //   dispatch(
    //     apiReduxApps.FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE.operations.forceStart(
    //       {
    //         data: { page, status, assigneeUserId },
    //       }
    //     )
    //   );
    // },
  };
};

const AgileBoard = connect(
  mapStateToProps,
  mapDispatchToProps
)(AgileBoardUnconnected);

export default AgileBoard;
