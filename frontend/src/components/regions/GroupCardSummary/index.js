import React, { useEffect } from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";
import { apiReduxApps } from "../../../apiAccess/redux/apiApps";

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

const GroupCardSummaryUnconnected = ({
  cards,
  userGroups,
  fetchSingleUserGroup,
  fetchUserGroupSummaryCards,
}) => {
  const { groupId } = useParams();
  const userGroup = userGroups[groupId];
  useEffect(() => {
    if (userGroup === undefined) {
      fetchSingleUserGroup({ groupId });
    } else {
      fetchUserGroupSummaryCards({ userGroup });
    }
  }, [userGroup, fetchSingleUserGroup, groupId, fetchUserGroupSummaryCards]);

  const studentUsers = getStudentUserDisplayData({ userGroup });

  const filteredCards = filteredCardsAsArray({
    cards,
    filterByUsers: studentUsers,
  });
  const props = {
    columns: getColumns({ cards: filteredCards }),
    rows: getRows({ cards: filteredCards, filterByUsers: studentUsers }),
    userGroup: userGroup || {},
    displayUsers: studentUsers,
  };

  return <Presentation {...props} />;
};

const mapStateToProps = (state) => {
  const cards = state.Entities.projectSummaryCards || {};
  const userGroups = state.Entities.userGroups || {};

  return {
    cards,
    userGroups,
  };
};
const mapDispatchToProps = (dispatch) => {
  return {
    fetchSingleUserGroup: ({ groupId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_USER_GROUP.operations.maybeStart({
          data: { groupId },
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
  };
};

const GroupCardSummary = connect(
  mapStateToProps,
  mapDispatchToProps
)(GroupCardSummaryUnconnected);

export default GroupCardSummary;
