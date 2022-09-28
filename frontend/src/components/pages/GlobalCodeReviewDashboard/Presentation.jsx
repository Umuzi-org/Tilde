import React from "react";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
// import Chip from "@material-ui/core/Chip";
import { makeStyles } from "@material-ui/core/styles";
import Button from "../../widgets/Button";
import Loading from "../../widgets/Loading";
import CompetenceReviewQueueEntry from "./CompetenceReviewQueueEntry";
import PullRequestReviewQueueEntry from "./PullRequestReviewQueueEntry";
import FilterByNames from "./FilterByNames";
import competenceProjects from "./mock-competence-review-projects";
import pullRequestProjects from "./mock-pull-request-review-projects";
import { useState } from "react";
import ReviewQueueFilterChips from "./ReviewQueueFilterChips";

const useStyles = makeStyles((theme) => {
  return {
    mainSection: {
      width: "100%",
      paddingTop: 0,
      height: "calc(100vh - 64px)",
    },
    queueContainer: {
      margin: 0,
      width: "100%",
    },
    queueItem: {
      maxHeight: "90vh",
      overflowY: "scroll",
      padding: "0px 10px",
    },
    queueContainerHeading: {
      position: "sticky",
      top: -5,
      padding: "10px 0px",
      backgroundColor: theme.palette.background.default,
      zIndex: 2,
      display: "flex",
      flexDirection: "column",
      gap: 10,
    },
    queueContainerHeadingFilters: {
      display: "flex",
      alignItems: "center",
      gap: 5,
      flexWrap: "wrap",
    },
  };
});

export default function Presentation({
  competenceReviewQueueProjects,
  pullRequestReviewQueueProjects,

  competenceReviewQueueLoading,
  pullRequestReviewQueueLoading,

  fetchNextCompetenceReviewQueuePage,
  fetchNextPullRequestQueuePage,

  filterIncludeTags,
  filterExcludeTags,

  filterIncludeFlavours,
  filterExcludeFlavours,

  handleChangeFlavourFilter,
  handleChangeTagFilter,

  teams,
  allTeamNames,
  filterIncludeAssigneeTeams,
  handleChangeAssigneeTeamFilter,
}) {
  const classes = useStyles();

  filterIncludeTags = filterIncludeTags || [];
  filterExcludeTags = filterExcludeTags || [];
  filterIncludeFlavours = filterIncludeFlavours || [];
  filterExcludeFlavours = filterExcludeFlavours || [];
  competenceReviewQueueProjects = competenceProjects || [];
  pullRequestReviewQueueProjects = pullRequestProjects || [];

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

  function applyFilters(project) {
    if (filterIncludeTags.length) {
      for (let tag of filterIncludeTags) {
        if (!project.tagNames.includes(tag)) return false;
      }
    }

    if (filterExcludeTags.length) {
      for (let tag of filterExcludeTags) {
        if (project.tagNames.includes(tag)) return false;
      }
    }
    if (filterIncludeFlavours.length) {
      for (let flavour of filterIncludeFlavours) {
        if (!project.flavourNames.includes(flavour)) return false;
      }
    }
    if (filterExcludeFlavours.length) {
      for (let flavour of filterExcludeFlavours) {
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

  const initialPullRequestOrderFilters = [
    {
      label: "last updated time(oldest)",
      sortFunction: (a, b) =>
        new Date(a.oldestOpenPrUpdatedTime) -
        new Date(b.oldestOpenPrUpdatedTime),
      isSelected: true,
    },
    {
      label: "last updated time(newest)",
      sortFunction: (a, b) =>
        new Date(b.oldestOpenPrUpdatedTime) -
        new Date(a.oldestOpenPrUpdatedTime),
      isSelected: false,
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

  const [selectedPullRequestOrderFilter, setSelectedPullRequestOrderFilter] =
    useState(() => {
      return pullRequestOrderFilters.filter(
        (orderFilter) => orderFilter.isSelected
      )[0];
    });

  const [selectedCompetenceOrderFilter, setSelectedCompetenceOrderFilter] =
    useState(() => {
      return competenceOrderFilters.filter(
        (orderFilter) => orderFilter.isSelected
      )[0];
    });

  // function ReviewQueueFilterChips({
  //   orderFilters,
  //   setFiltersMethod,
  //   setSelectedFilterMethod,
  // }) {
  //   return (
  //     <>
  //       <Typography>Sort by:</Typography>
  //       {orderFilters &&
  //         orderFilters.map((filter) => (
  //           <Chip
  //             label={filter.label}
  //             variant={filter.isSelected ? "default" : "outlined"}
  //             onClick={() =>
  //               handleClick({
  //                 setFiltersMethod: setFiltersMethod,
  //                 setSelectedFilterMethod: setSelectedFilterMethod,
  //                 selectedFilter: filter,
  //               })
  //             }
  //           />
  //         ))}
  //     </>
  //   );
  // }

  // function handleClick({
  //   setFiltersMethod,
  //   setSelectedFilterMethod,
  //   selectedFilter,
  // }) {
  //   setFiltersMethod((prev) => {
  //     return prev.map((filter) => {
  //       if (filter.label === selectedFilter.label) {
  //         const newSelectedFilter = { ...filter, isSelected: true };
  //         setSelectedFilterMethod(newSelectedFilter);
  //         return { ...filter, isSelected: true };
  //       } else {
  //         return { ...filter, isSelected: false };
  //       }
  //     });
  //   });
  // }

  return (
    <Grid container spacing={3} className={classes.mainSection}>
      <Grid item xs={2}>
        <Typography variant="h6">Filter by flavour</Typography>
        <Paper>
          <FilterByNames
            allNames={allFlavours}
            filterInclude={filterIncludeFlavours}
            filterExclude={filterExcludeFlavours}
            onChange={handleChangeFlavourFilter}
          />
        </Paper>

        <Typography variant="h6">Filter by tag</Typography>
        <Paper>
          <FilterByNames
            allNames={allTagNames}
            filterInclude={filterIncludeTags}
            filterExclude={filterExcludeTags}
            onChange={handleChangeTagFilter}
          />
        </Paper>

        <Typography variant="h6">Filter by assignee team</Typography>
        <Paper>
          <FilterByNames
            allNames={allTeamNames}
            filterInclude={filterIncludeAssigneeTeams}
            filterExclude={[]}
            onChange={handleChangeAssigneeTeamFilter}
          />
        </Paper>
      </Grid>
      <Grid item xs={10} container className={classes.queueContainer}>
        <Grid item xs={12} md={6} className={classes.queueItem}>
          {/* TODO center headings*/}
          <Grid className={classes.queueContainerHeading}>
            <Typography variant="h5">Competence Review Queue</Typography>
            <Grid className={classes.queueContainerHeadingFilters}>
              <ReviewQueueFilterChips
                orderFilters={competenceOrderFilters}
                setFiltersMethod={setCompetenceOrderFilters}
                setSelectedFilterMethod={setSelectedCompetenceOrderFilter}
              />
            </Grid>
          </Grid>
          <Grid>
            {competenceReviewQueueProjects
              .filter(applyFilters)
              .sort(selectedCompetenceOrderFilter.sortFunction)
              .map((project) => (
                <CompetenceReviewQueueEntry project={project} />
              ))}
          </Grid>
          <Paper elevation={3} className={classes.project} variant="outlined">
            {competenceReviewQueueLoading ? (
              <Loading />
            ) : (
              <Button onClick={fetchNextCompetenceReviewQueuePage}>
                Load more
              </Button>
            )}
            {/* TODO Center the button or spinner*/}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6} className={classes.queueItem}>
          <Grid className={classes.queueContainerHeading}>
            <Typography variant="h5">Pull Request Review Queue</Typography>
            <Grid className={classes.queueContainerHeadingFilters}>
              <ReviewQueueFilterChips
                orderFilters={pullRequestOrderFilters}
                setFiltersMethod={setPullRequestOrderFilters}
                setSelectedFilterMethod={setSelectedPullRequestOrderFilter}
              />
            </Grid>
          </Grid>
          <Grid>
            {pullRequestReviewQueueProjects
              .filter(applyFilters)
              .sort(selectedPullRequestOrderFilter.sortFunction)
              .map((project) => (
                <PullRequestReviewQueueEntry project={project} />
              ))}
          </Grid>

          <Paper elevation={3} className={classes.project} variant="outlined">
            {pullRequestReviewQueueLoading ? (
              <Loading />
            ) : (
              <Button onClick={fetchNextPullRequestQueuePage}>Load more</Button>
            )}
            {/* TODO Center the button or spinner*/}
          </Paper>
        </Grid>
      </Grid>
    </Grid>
  );
}
