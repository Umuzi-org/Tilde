import React from "react";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../apiAccess/redux/apiApps";
import Presentation from "./Presentation";

function RepositoryDetailsUnconnected({
  repositoryId,
  repositories,
  fetchRepository,
  fetchCommits,
  fetchPullRequests,
  commits,
  pullRequests,
}) {
  React.useEffect(() => {
    if (repositoryId) {
      fetchRepository({ repositoryId });
      fetchCommits({ repositoryId });
      fetchPullRequests({ repositoryId });
    }
  }, [repositoryId, fetchRepository, fetchCommits, fetchPullRequests]);
  const [tabValue, setTabValue] = React.useState(0);

  const handleChangeTab = (event, newValue) => {
    setTabValue(newValue);
  };

  const repository = repositories[repositoryId];
  const currentCommits = Object.values(commits).filter(
    (commit) => commit.repository === repositoryId
  );
  const currentPullRequests = Object.values(pullRequests).filter(
    (pr) => pr.repository === repositoryId
  );

  const props = {
    repository,
    currentCommits,
    currentPullRequests,
    tabValue,
    handleChangeTab,
  };
  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    repositories:
      state.Entities.repositories === undefined
        ? {}
        : state.Entities.repositories,
    commits:
      state.Entities.repoCommits === undefined
        ? {}
        : state.Entities.repoCommits,
    pullRequests:
      state.Entities.pullRequests === undefined
        ? {}
        : state.Entities.pullRequests,
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
