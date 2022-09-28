import React from "react";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import Chip from "@material-ui/core/Chip";
import { makeStyles } from "@material-ui/core/styles";
import Button from "../../widgets/Button";
import Loading from "../../widgets/Loading";
import CompetenceReviewQueueEntry from "./CompetenceReviewQueueEntry";
import PullRequestReviewQueueEntry from "./PullRequestReviewQueueEntry";
import FilterByNames from "./FilterByNames";
import competenceProjects from "./mock-competence-review-projects";
import pullRequestProjects from "./mock-pull-request-review-projects";
import { useState } from "react";
import { useEffect } from "react";

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

  const [pullRequestOrderFilters, setPullRequestOrderFilters] = useState(
    initialPullRequestOrderFilters
  );

  const [selectedPullRequestOrderFilter, setSelectedPullRequestOrderFilter] =
    useState({});

  useEffect(() => {
    const selectedfilter = pullRequestOrderFilters.filter(
      (orderFilter) => orderFilter.isSelected
    );
    setSelectedPullRequestOrderFilter(selectedfilter[0]);
  }, [selectedPullRequestOrderFilter]);

  function QueueFilterChips({ orderFilters }) {
    return (
      orderFilters &&
      orderFilters.map((filter) => (
        <Chip
          label={filter.label}
          variant={filter.isSelected ? "default" : "outlined"}
          onClick={() =>
            handleClick({
              selectedFilter: filter,
            })
          }
        />
      ))
    );
  }

  function handleClick({ selectedFilter }) {
    setPullRequestOrderFilters((prev) => {
      return prev.map((filter) => {
        if (filter.label === selectedFilter.label) {
          const newSelectedFilter = { ...filter, isSelected: true };
          setSelectedPullRequestOrderFilter(newSelectedFilter);
          return { ...filter, isSelected: true };
        } else {
          return { ...filter, isSelected: false };
        }
      });
    });
  }

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
          </Grid>
          <Grid>
            {/* TODO improve scrolling behavior: keep the heading in view, just scroll the items */}
            {competenceReviewQueueProjects
              .filter(applyFilters)
              .sort(
                (a, b) =>
                  new Date(a.reviewRequestTime) - new Date(b.reviewRequestTime)
              )
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
            <Grid>
              <QueueFilterChips orderFilters={pullRequestOrderFilters} />
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
