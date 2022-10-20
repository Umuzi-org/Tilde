import React, { useEffect } from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";

import { apiReduxApps } from "../../../apiAccess/apiApps";
import { apiUtilitiesOperations } from "../../../apiAccess/redux";

import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";
import { useState } from "react";

function removeNameFromArray({ array, name }) {
  const index = array.indexOf(name);
  if (index !== -1) {
    array.splice(index, 1);
  }
  return array;
}

function filterByCardName(allCards, cardName) {
  if (cardName) {
    return allCards.filter((card) =>
      card.contentItemTitle.toLowerCase().includes(cardName.toLowerCase())
    );
  }
  return allCards;
}

function GlobalCodeReviewDashboardUnconnected({
  // mapStateToProps

  competenceReviewQueueProjectsObject,
  pullRequestReviewQueueProjectsObject,
  FETCH_COMPETENCE_REVIEW_QUEUE_PAGE,
  FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE,
  teams,

  // mapDispatchToProps

  fetchCompetenceReviewQueuePage,
  fetchPullRequestReviewQueuePage,
  fetchTeamsPages,
}) {
  teams = teams || {};

  const [filterIncludeTags, setFilterIncludeTags] = useState([]);
  const [filterExcludeTags, setFilterExcludeTags] = useState([
    "technical-assessment",
  ]);

  const [filterIncludeFlavours, setFilterIncludeFlavours] = useState([]);
  const [filterExcludeFlavours, setFilterExcludeFlavours] = useState([]);

  const [filterIncludeAssigneeTeams, setFilterIncludeAssigneeTeams] = useState(
    []
  );

  const initialPullRequestOrderFilters = [
    {
      label: "last updated time",
      sortFunction: (a, b) =>
        new Date(a.oldestOpenPrUpdatedTime) -
        new Date(b.oldestOpenPrUpdatedTime),
      isSelected: true,
    },
  ];

  const initialCompetenceOrderFilters = [
    {
      label: "review request time",
      sortFunction: (a, b) =>
        new Date(a.reviewRequestTime) - new Date(b.reviewRequestTime),
      isSelected: true,
    },
    {
      label: "start time",
      sortFunction: (a, b) => new Date(a.startTime) - new Date(b.startTime),
      isSelected: false,
    },
    {
      label: "positive reviews",
      sortFunction: (a, b) => {
        return (
          b.codeReviewCompetentSinceLastReviewRequest +
          b.codeReviewExcellentSinceLastReviewRequest -
          (a.codeReviewCompetentSinceLastReviewRequest +
            a.codeReviewExcellentSinceLastReviewRequest)
        );
      },
      isSelected: false,
    },
  ];

  const [pullRequestOrderFilters, setPullRequestOrderFilters] = useState(
    initialPullRequestOrderFilters
  );

  const [competenceOrderFilters, setCompetenceOrderFilters] = useState(
    initialCompetenceOrderFilters
  );

  const [
    selectedPullRequestOrderFilter,
    setSelectedPullRequestOrderFilter,
  ] = useState(() => {
    return pullRequestOrderFilters.filter(
      (orderFilter) => orderFilter.isSelected
    )[0];
  });

  const [
    selectedCompetenceOrderFilter,
    setSelectedCompetenceOrderFilter,
  ] = useState(() => {
    return competenceOrderFilters.filter(
      (orderFilter) => orderFilter.isSelected
    )[0];
  });

  const [cardNameSearchValue, setCardNameSearchValue] = useState("");

  useEffect(() => {
    fetchCompetenceReviewQueuePage({ page: 1 });
    fetchPullRequestReviewQueuePage({ page: 1 });
    fetchTeamsPages();
  }, [
    fetchCompetenceReviewQueuePage,
    fetchPullRequestReviewQueuePage,
    fetchTeamsPages,
  ]);

  const fetchCompetenceReviewQueueLastCall = getLatestMatchingCall({
    callLog: FETCH_COMPETENCE_REVIEW_QUEUE_PAGE,
  }) || { loading: true };

  const fetchPullRequestQueueLastCall = getLatestMatchingCall({
    callLog: FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE,
  }) || { loading: true };

  const competenceReviewQueueProjects = Object.values(
    competenceReviewQueueProjectsObject || {}
  );

  const pullRequestReviewQueueProjects = Object.values(
    pullRequestReviewQueueProjectsObject || {}
  );

  const allFlavours = [
    ...new Set(
      [
        ...competenceReviewQueueProjects.map((proj) => proj.flavourNames),
        pullRequestReviewQueueProjects.map((proj) => proj.flavourNames),
      ]
        .flat()
        .flat() // yes, twice
    ),
  ].sort();

  const allTagNames = [
    ...new Set(
      [
        ...competenceReviewQueueProjects.map((proj) => proj.tagNames),
        pullRequestReviewQueueProjects.map((proj) => proj.tagNames),
      ]
        .flat()
        .flat() // yes, twice
    ),
  ].sort();

  const allTeamNames = Object.values(teams)
    .map((o) => o.name)
    .sort();

  function applyFilters(project) {
    if (filterIncludeTags.length) {
      for (const tag of filterIncludeTags) {
        if (!project.tagNames.includes(tag)) return false;
      }
    }

    if (filterExcludeTags.length) {
      for (const tag of filterExcludeTags) {
        if (project.tagNames.includes(tag)) return false;
      }
    }
    if (filterIncludeFlavours.length) {
      for (const flavour of filterIncludeFlavours) {
        if (!project.flavourNames.includes(flavour)) return false;
      }
    }
    if (filterExcludeFlavours.length) {
      for (const flavour of filterExcludeFlavours) {
        if (project.flavourNames.includes(flavour)) return false;
      }
    }

    if (filterIncludeAssigneeTeams.length) {
      const includedUserIds = Object.values(teams)
        .filter((team) => filterIncludeAssigneeTeams.includes(team.name))
        .map((team) => team.members)
        .flat()
        .map((o) => o.userId);

      const intersection = project.recruitUsers.filter((value) =>
        includedUserIds.includes(value)
      );
      if (intersection.length === 0) return false;
    }

    return true;
  }

  function fetchNextCompetenceReviewQueuePage() {
    const page = fetchCompetenceReviewQueueLastCall.requestData.page + 1;
    fetchCompetenceReviewQueuePage({ page });
  }

  function fetchNextPullRequestQueuePage() {
    const page = fetchPullRequestQueueLastCall.requestData.page + 1;
    fetchPullRequestReviewQueuePage({ page });
  }

  function handleChangeFilter({
    includes,
    excludes,
    setIncludes,
    setExcludes,
  }) {
    excludes = excludes || [];
    function handleChangeFlavourFilter(name) {
      function handle() {
        if (includes.includes(name)) {
          const newFilterIncludes = removeNameFromArray({
            array: includes,
            name,
          });
          setIncludes([...newFilterIncludes]);
          if (setExcludes) setExcludes([...excludes, name]);
        } else if (excludes.includes(name)) {
          const newFilterExcludes = removeNameFromArray({
            array: excludes,
            name,
          });
          setExcludes([...newFilterExcludes]);
        } else {
          setIncludes([...includes, name]);
        }
      }
      return handle;
    }
    return handleChangeFlavourFilter;
  }

  const handleChangeFlavourFilter = handleChangeFilter({
    includes: filterIncludeFlavours,
    excludes: filterExcludeFlavours,
    setIncludes: setFilterIncludeFlavours,
    setExcludes: setFilterExcludeFlavours,
  });

  const handleChangeTagFilter = handleChangeFilter({
    includes: filterIncludeTags,
    excludes: filterExcludeTags,
    setIncludes: setFilterIncludeTags,
    setExcludes: setFilterExcludeTags,
  });

  const handleChangeAssigneeTeamFilter = handleChangeFilter({
    includes: filterIncludeAssigneeTeams,
    setIncludes: setFilterIncludeAssigneeTeams,
  });

  function handleChangeCardNameSearchValue(e) {
    setCardNameSearchValue(e.target.value);
  }

  const props = {
    competenceReviewQueueProjects: filterByCardName(
      competenceReviewQueueProjects,
      cardNameSearchValue
    ),
    pullRequestReviewQueueProjects: filterByCardName(
      pullRequestReviewQueueProjects,
      cardNameSearchValue
    ),

    competenceReviewQueueLoading: fetchCompetenceReviewQueueLastCall.loading,
    pullRequestReviewQueueLoading: fetchPullRequestQueueLastCall.loading,

    fetchNextCompetenceReviewQueuePage,
    fetchNextPullRequestQueuePage,

    filterIncludeTags,
    filterExcludeTags,

    filterIncludeFlavours,
    filterExcludeFlavours,

    allFlavours,
    allTagNames,
    applyFilters,

    competenceOrderFilters,
    setCompetenceOrderFilters,
    selectedCompetenceOrderFilter,
    setSelectedCompetenceOrderFilter,

    pullRequestOrderFilters,
    setPullRequestOrderFilters,
    selectedPullRequestOrderFilter,
    setSelectedPullRequestOrderFilter,

    handleChangeFlavourFilter,
    handleChangeTagFilter,

    allTeamNames,
    filterIncludeAssigneeTeams,
    handleChangeAssigneeTeamFilter,

    cardNameSearchValue,
    handleChangeCardNameSearchValue,
  };
  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    competenceReviewQueueProjectsObject:
      state.apiEntities.competenceReviewQueueProject,
    pullRequestReviewQueueProjectsObject:
      state.apiEntities.pullRequestReviewQueueProject,
    FETCH_COMPETENCE_REVIEW_QUEUE_PAGE:
      state.FETCH_COMPETENCE_REVIEW_QUEUE_PAGE,
    FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE:
      state.FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE,
    teams: state.apiEntities.teams,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchCompetenceReviewQueuePage: ({ page }) => {
      dispatch(
        apiReduxApps.FETCH_COMPETENCE_REVIEW_QUEUE_PAGE.operations.maybeStart({
          data: { page },
        })
      );
    },

    fetchPullRequestReviewQueuePage: ({ page }) => {
      dispatch(
        apiReduxApps.FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE.operations.maybeStart(
          {
            data: { page },
          }
        )
      );
    },

    fetchTeamsPages: () => {
      const data = { page: 1 };
      dispatch(
        apiReduxApps.FETCH_TEAMS_PAGE.operations.maybeStart({
          data,

          successDispatchActions: [
            apiUtilitiesOperations.fetchAllPages({
              API_BASE_TYPE: "FETCH_TEAMS_PAGE",
              requestData: data,
            }),
          ],
        })
      );
    },
  };
};

const GlobalCodeReviewDashboard = connect(
  mapStateToProps,
  mapDispatchToProps
)(GlobalCodeReviewDashboardUnconnected);

export default GlobalCodeReviewDashboard;
