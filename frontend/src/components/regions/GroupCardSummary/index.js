import React, { useEffect } from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";
import { apiReduxApps } from "../../../apiAccess/redux/apiApps";
import { getLatestMatchingCall } from "../../../utils/ajaxRedux";

const arrayToObjectWithIdKeys = ({ data }) => {
  let dataAsObject = {};

  data.forEach((element) => {
    dataAsObject[element.id] = element;
  });
  return dataAsObject;
};

const getColumns = ({ cards }) => {
  const sortedUniqueContentIds = cards
    .map((card) => card.contentItem)
    .filter((v, i, a) => a.indexOf(v) === i);

  const contentAsObject = arrayToObjectWithIdKeys({
    data: cards.map((card) => {
      return {
        id: card.contentItem,
        title: card.title,
        url: card.contentItemUrl,
        order: card.order,
      };
    }),
  });

  return sortedUniqueContentIds
    .map((id) => {
      return {
        url: contentAsObject[id].url,
        label: contentAsObject[id].title,
        order: contentAsObject[id].order,
        id,
      };
    })
    .sort((card1, card2) => card1.order - card2.order);
};

const getRows = ({ cards, filterByUsers }) => {
  const userIds = cards
    .map((card) => card.assignees)
    .flat()
    .filter((v, i, a) => a.indexOf(v) === i)
    .filter((value) => filterByUsers[value])
    .sort();

  let rows = {};

  for (let userId of userIds) {
    rows[userId] = {};
  }

  for (let card of cards) {
    for (let userId of card.assignees) {
      if (rows[userId] !== undefined) {
        rows[userId][card.contentItem] = card;
      }
    }
  }

  return rows;
};

const filteredCardsAsArray = ({ cards, filterByUsers }) => {
  return Object.values(cards).filter((card) => {
    for (let assignee of card.assignees) {
      if (filterByUsers[assignee]) return true;
    }
    return false;
  });
};

const getStudentUserDisplayData = ({ userGroup }) => {
  if (!userGroup) return {};
  let ret = {};
  userGroup.members.forEach((member) => {
    ret[member.userId] = member.userEmail;
  });
  return ret;
};

function getApiCallData({
  userGroup,
  FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE,
}) {
  if (!userGroup) return {};
  let ret = {};
  userGroup.members.forEach((member) => {
    ret[member.userId] = getLatestMatchingCall({
      callLog: FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE,
      requestData: {
        assigneeUserId: member.userId,
      },
    }) || { loading: true };
  });
  return ret;
}

const GroupCardSummaryUnconnected = ({
  cards,
  teams,
  FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE,
  fetchSingleUserGroup,
  fetchUserGroupSummaryCards,
  fetchUserGroupSummaryCardsByDataSequence,
}) => {
  const { teamId } = useParams();
  const userGroup = teams[teamId];

  useEffect(() => {
    if (userGroup === undefined) {
      fetchSingleUserGroup({ teamId });
    } else {
      fetchUserGroupSummaryCards({ userGroup });
    }
  }, [userGroup, fetchSingleUserGroup, teamId, fetchUserGroupSummaryCards]);

  const apiCallData = userGroup
    ? getApiCallData({
        userGroup,
        FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE,
      })
    : {};

  const studentUsers = getStudentUserDisplayData({ userGroup });

  const filteredCards = filteredCardsAsArray({
    cards,
    filterByUsers: studentUsers,
  });

  const rows = getRows({ cards: filteredCards, filterByUsers: studentUsers });

  function fetchNextPages() {
    // if anything is still loading then chill
    for (let userId in apiCallData) {
      if (apiCallData[userId].loading) return;
    }

    let dataSequence = [];
    for (let userId in apiCallData) {
      if (apiCallData[userId].responseData.results.length > 0) {
        dataSequence.push({
          assigneeUserId: parseInt(userId),
          page: apiCallData[userId].requestData.page + 1,
        });
      }
    }

    fetchUserGroupSummaryCardsByDataSequence({ dataSequence });
  }
  function handleScroll(e) {
    const atRight =
      e.target.scrollLeft + e.target.clientWidth >= e.target.scrollWidth;

    if (atRight) {
      fetchNextPages();
    }
  }

  const props = {
    columns: getColumns({ cards: filteredCards }),
    rows,
    apiCallData,
    userGroup: userGroup || {},
    displayUsers: studentUsers,
    handleScroll,
  };

  return <Presentation {...props} />;
};

const mapStateToProps = (state) => {
  const cards = state.Entities.projectSummaryCards || {};
  const teams = state.Entities.teams || {};
  const { FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE } = state;

  return {
    cards,
    teams,
    FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE,
  };
};
const mapDispatchToProps = (dispatch) => {
  return {
    fetchSingleUserGroup: ({ teamId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_TEAM.operations.maybeStart({
          data: { teamId },
        })
      );
    },

    fetchUserGroupSummaryCards: ({ userGroup }) => {
      const dataSequence = userGroup.members.map((member) => {
        return { assigneeUserId: member.userId, page: 1 };
      });
      dispatch(
        apiReduxApps.FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE.operations.maybeStartCallSequence(
          { dataSequence }
        )
      );
    },

    fetchUserGroupSummaryCardsByDataSequence({ dataSequence }) {
      dispatch(
        apiReduxApps.FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE.operations.maybeStartCallSequence(
          { dataSequence }
        )
      );
    },
  };
};

const GroupCardSummary = connect(
  mapStateToProps,
  mapDispatchToProps
)(GroupCardSummaryUnconnected);

export default GroupCardSummary;
