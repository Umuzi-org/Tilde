import React from "react";
import { connect } from "react-redux";
import Presentation from "./Presentation.js";
import { apiReduxApps } from "../../../apiAccess/redux/apiApps";
import operations from "./redux/operations.js";

function anyLoading({ callLog }) {
  if (callLog.length === 0) return true;
  for (let entry of callLog) {
    if (entry.loading) return true;
  }
  return false;
}

function AppFilterUnconnected({
  FETCH_COHORTS_PAGE,
  fetchCohortsPages,
  cohorts,
  setAppFilterByUserId,
  setAppFilterByCohortId,
}) {
  React.useEffect(() => {
    fetchCohortsPages({
      dataSequence: [{ page: 1 }, { page: 2 }],
    });
  });

  const loading = anyLoading({ callLog: FETCH_COHORTS_PAGE });

  const [viewCohortId, setViewCohortId] = React.useState(null);
  const [viewRecruitUserEmail, setViewRecruitUserEmail] = React.useState(null);

  const [filterByRecruitValue, setFilterByRecruitValue] = React.useState("");
  const [filterByCohortValue, setFilterByCohortValue] = React.useState("");

  const cohortNiceName = (cohort) =>
    `${cohort.cohortNumber} ${cohort.curriculumName}`;

  const cohortsNice = Object.keys(cohorts).map((cohortId) => {
    const betterCohort = {
      ...cohorts[cohortId],
      label: cohortNiceName(cohorts[cohortId]),
      filteredCohortRecruitUserEmails: filterByRecruitValue
        ? cohorts[cohortId].cohortRecruitUserEmails.filter(
            (value) => value.indexOf(filterByRecruitValue) !== -1
          )
        : cohorts[cohortId].cohortRecruitUserEmails,
    };
    return betterCohort;
  });

  const filteredNiceCohrts = cohortsNice.filter((cohort) => {
    if (filterByCohortValue) {
      return cohort.label.indexOf(filterByCohortValue) !== -1;
    } else return true;
  });

  const currentCohort = cohortsNice.find(
    (cohort) => cohort.id === viewCohortId
  );

  const handleChangeFilterByCohort = (event) => {
    // for text filtering
    setFilterByCohortValue(event.target.value);
  };

  const handleChangeFilterByRecruit = (event) => {
    // for text filtering
    setFilterByRecruitValue(event.target.value);
  };

  const handleSelectCohortToView = (cohortId) => {
    setViewCohortId(cohortId);
    setAppFilterByCohortId({ cohortId });
  };

  const handleSelectRecruitToView = (userEmail) => {
    setViewRecruitUserEmail(userEmail);

    const userIndex = currentCohort.cohortRecruitUserEmails.indexOf(userEmail);

    if (userIndex === -1)
      throw new Error(
        "The selected email isn't in the selected cohort. Friggin weird"
      );

    const userId = currentCohort.cohortRecruitUsers[userIndex];
    setAppFilterByUserId({ userId });
  };
  const props = {
    // appFilter,
    cohorts: filteredNiceCohrts,
    handleSelectCohortToView,

    filterByRecruitValue,
    filterByCohortValue,
    handleChangeFilterByCohort,
    handleChangeFilterByRecruit,

    currentCohort,

    viewCohortId,

    handleSelectRecruitToView,
    viewRecruitUserEmail,
    loading,
  };
  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    authUser: state.App.authUser,
    appFilter: state.App.appFilter,
    FETCH_COHORTS_PAGE: state.FETCH_COHORTS_PAGE,
    cohorts: state.Entities.cohorts || {},
  };
};

const mapDispatchToProps = (dispatch) => {
  const fetchCohortsPages = ({ dataSequence }) => {
    dispatch(
      apiReduxApps.FETCH_COHORTS_PAGE.operations.maybeStartCallSequence({
        dataSequence,
      })
    );
  };

  const setAppFilterByUserId = ({ userId }) => {
    dispatch(operations.setFilterByUserId({ userId }));
  };

  const setAppFilterByCohortId = ({ cohortId }) => {
    dispatch(operations.setFilterByCohortId({ cohortId }));
  };

  return { fetchCohortsPages, setAppFilterByUserId, setAppFilterByCohortId };
};

const AppFilter = connect(
  mapStateToProps,
  mapDispatchToProps
)(AppFilterUnconnected);

export default AppFilter;
