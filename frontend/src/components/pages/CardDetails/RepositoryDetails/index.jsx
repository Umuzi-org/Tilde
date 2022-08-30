import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../../apiAccess/apiApps";
import Presentation from "./Presentation";
import Loading from "../../../widgets/Loading";

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
  fetchCommits,
  fetchPullRequests,
  commits,
  pullRequests,
}) {
  useEffect(() => {
    if (repositoryId) {
      fetchRepository({ repositoryId });
      // fetchCommits({ repositoryId });
      fetchPullRequests({ repositoryId });
    }
  }, [repositoryId, fetchRepository, fetchCommits, fetchPullRequests]);
  const [tabValue, setTabValue] = useState(0);

  const handleChangeTab = (event, newValue) => {
    setTabValue(newValue);
  };

  const repository = repositories[repositoryId];
  const currentCommits = Object.values(commits).filter(
    (commit) => commit.repository === repositoryId
  );
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
    currentCommits,
    currentPullRequests,
    tabValue,
    handleChangeTab,
  };
  console.log("Mumbo")
  return <Loading />;
  // return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    repositories:
      state.apiEntities.repositories === undefined
        ? {}
        : state.apiEntities.repositories,
    commits:
      state.apiEntities.repoCommits === undefined
        ? {}
        : state.apiEntities.repoCommits,
    pullRequests:
      state.apiEntities.pullRequests === undefined
        ? {}
        : state.apiEntities.pullRequests,
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
    fetchCommits: ({ repositoryId }) => {
      dispatch(
        apiReduxApps.FETCH_COMMITS_PAGE.operations.maybeStart({
          data: { repositoryId, page: 1 },
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
