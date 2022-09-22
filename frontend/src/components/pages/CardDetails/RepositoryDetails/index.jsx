import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../../apiAccess/apiApps";
import Presentation from "./Presentation";

function toLocaleString(dateTimeString) {
  if (dateTimeString) {
    const timestamp = new Date(dateTimeString);
    return timestamp.toLocaleString();
  } else return null;
}

function RepositoryDetailsUnconnected({
  repositoryId,
  repositories,
  fetchRepository,
  fetchPullRequests,
  pullRequests,
}) {
  repositories = repositories || {};
  pullRequests = pullRequests || {};

  useEffect(() => {
    if (repositoryId) {
      fetchRepository({ repositoryId });
      fetchPullRequests({ repositoryId });
    }
  }, [repositoryId, fetchRepository, fetchPullRequests]);

  const [tabValue, setTabValue] = useState(0);

  const handleChangeTab = (event, newValue) => {
    setTabValue(newValue);
  };

  const repository = repositories[repositoryId];

  const currentPullRequests = Object.values(pullRequests)
    .filter((pr) => pr.repository === repositoryId)
    .map((pr) => {
      return {
        ...pr,
        updatedAt: toLocaleString(pr.updatedAt),
        closedAt: toLocaleString(pr.closedAt),
        mergedAt: toLocaleString(pr.mergedAt),
        createdAt: toLocaleString(pr.createdAt),
      };
    });

  const props = {
    repository,
    currentPullRequests,
    tabValue,
    handleChangeTab,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    repositories: state.apiEntities.repositories,
    pullRequests: state.apiEntities.pullRequests,
  };
};
const mapDispatchToProps = (dispatch) => {
  return {
    fetchRepository: ({ repositoryId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_REPOSITORY.operations.maybeStart({
          data: { repositoryId },
        })
      );
    },

    fetchPullRequests: ({ repositoryId }) => {
      dispatch(
        apiReduxApps.FETCH_PULL_REQUESTS_PAGE.operations.maybeStart({
          data: { repositoryId, page: 1 },
        })
      );
    },
  };
};
const RepositoryDetails = connect(
  mapStateToProps,
  mapDispatchToProps
)(RepositoryDetailsUnconnected);
export default RepositoryDetails;
