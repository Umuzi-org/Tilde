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

const getRows = ({ cards }) => {
  const names = cards
    .map((card) => card.assigneeNames)
    .flat()
    .filter((v, i, a) => a.indexOf(v) === i)
    .sort();

  let rows = {};

  for (let name of names) {
    rows[name] = {};
  }

  for (let card of cards) {
    for (let name of card.assigneeNames) {
      rows[name][card.contentItem] = card;
    }
  }

  return rows;
};

const filteredCardsAsArray = ({ cards, userGroup }) => {
  if (userGroup === undefined) return [];
  const groupUsers = userGroup.members.map((member) => member.userId);
  return Object.values(cards).filter((card) => {
    for (let assignee of card.assignees) {
      if (groupUsers.indexOf(assignee) !== -1) return true;
    }
    return false;
  });
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
  });

  const filteredCards = filteredCardsAsArray({ cards, userGroup });
  const props = {
    columns: getColumns({ cards: filteredCards }),
    rows: getRows({ cards: filteredCards }),
    userGroup: userGroup || {},
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
      const dataSequence = userGroup.members
        .filter((member) => member.permissionStudent || true) // TODO: fix data
        .map((member) => {
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
