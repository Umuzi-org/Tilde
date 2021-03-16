import React, { useEffect } from "react";
import Presentation from "./Presentation";
import { apiReduxApps } from "../../../apiAccess/redux/apiApps";
import { connect } from "react-redux";
import consts from "../../../constants";
import { useParams } from "react-router-dom";
import { getLatestMatchingCall } from "../../../utils/ajaxRedux";
import Loading from "../../widgets/Loading";

// TODO: display loading spinner while fetching page
// TODO: scroll down to load more
// TODO: look nice

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

function getAllLatestCalls({
  FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
  userId,
}) {
  let result = {};

  const defaultCallLogEntry = { loading: true, requestData: { page: 0 } };

  for (let status in consts.AGILE_CARD_STATUS_CHOICES) {
    let current = {
      anyLoading: false,
      lastAssigneeCallPage: 0,
      lastReviewerCallPage: 0,
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

    if (consts.AGILE_CARD_STATUS_CHOICES_SHOW_REVIEWER.includes(status)) {
      const lastReviewerCall =
        getLatestMatchingCall({
          callLog: FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
          requestData: {
            reviewerUserId: userId,
            status,
          },
        }) || defaultCallLogEntry;

      current.anyLoading = current.anyLoading || lastReviewerCall.loading;
      current.lastReviewerCallPage = lastReviewerCall.requestData.page;
    }

    result[status] = { ...current };
    // console.log("=========================");
    // console.log(status);
    // console.log(current);
  }
  return result;
}

/*
Given a bunch of info from getAllLatestCalls, return a 
list of column titles which should contain loading spinners */
function columnsLoading({ latestCallStates }) {
  const result = Object.keys(consts.AGILE_COLUMNS).filter((columnName) => {
    for (let status of consts.AGILE_COLUMNS[columnName]) {
      if (latestCallStates[status].anyLoading) return true;
    }
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
  // fetchUser,
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

  const latestCallStates = getAllLatestCalls({
    FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
    userId,
  });

  function fetchNextColumnPage({ columnLabel }) {
    // console.log(columnLabel);
    const statuses = consts.AGILE_COLUMNS[columnLabel];

    let callSequenceData = [];

    for (let status of statuses) {
      if (consts.AGILE_CARD_STATUS_CHOICES_SHOW_REVIEWER.includes(status)) {
        // we need to also fetch the next review page
      }
    }
  }

  //   for (let status of statuses) {
  //     let assignedPageNumber = getLatestCallNextPageValue({
  //       FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
  //       status,
  //       assigneeUserId: userId,
  //     });

  //     if (assignedPageNumber !== null) {
  //       callSequenceData.push({
  //         page: assignedPageNumber,
  //         status,
  //         assigneeUserId: userId,
  //       });
  //     }

  //     let reviewPageNumber = getLatestCallNextPageValue({
  //       FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
  //       status,
  //       reviewerUserId: userId,
  //     });
  //     if (reviewPageNumber !== null) {
  //       callSequenceData.push({
  //         page: reviewPageNumber,
  //         status,
  //         reviewerUserId: userId,
  //       });
  //     }
  //   }

  // fetchCardPages({ dataSequence: callSequenceData });
  // }

  function handleColumnScroll({ column }) {
    function eventHandler(e) {
      const atBottom =
        e.target.scrollTop + e.target.clientHeight === e.target.scrollHeight;

      if (atBottom) {
        // console.log("At bottom")
        fetchNextColumnPage({ columnLabel: column.label });
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
    board: boardFromCards({ cards: filteredCards }),
    columnsLoading: columnsLoading({ latestCallStates }),
    viewedUser: users[userId],

    handleColumnScroll,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    users: state.Entities.users || {},
    cards: state.Entities.cards || {},
    FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE:
      state.FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
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

    fetchUser: ({ userId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_USER.operations.maybeStart({
          data: { userId },
        })
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
