import React from "react";
import Presentation from "./Presentation";

import { connect } from "react-redux";

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

function ProjectReportUnconnected({ cards }) {
  const props = {
    columns: getColumns({ cards }),
    rows: getRows({ cards }),
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  const { cohortId } = state.AppFilter;

  let cards = [];

  if (cohortId) {
    const cohortUsers = state.Entities.cohorts[cohortId].cohortRecruitUsers;
    const cardsObj = state.Entities.projectSummaryCards || {};
    cards = Object.values(cardsObj).filter((card) => {
      for (let assignee of card.assignees) {
        if (cohortUsers.indexOf(assignee) !== -1) return true;
      }
      return false;
    });
  }

  return {
    // authUser: state.ProjectReport.authUser,
    // whoAmICallStatus: state.WHO_AM_I,

    cards,
  };
};

const mapDispatchToProps = (dispatch) => {
  //   const whoAmIStart = (data) => {
  //     dispatch(apiReduxApps.FETCH_RECRUIT_PROJECTS_PAGE.operations.start(data));
  //   };

  //   return { whoAmIStart };
  return {};
};

const ProjectReport = connect(
  mapStateToProps,
  mapDispatchToProps
)(ProjectReportUnconnected);

export default ProjectReport;
