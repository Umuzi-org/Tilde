import React from "react";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/core/styles";
import Button from "../../widgets/Button";
import Loading from "../../widgets/Loading";
import CompetenceReviewQueueEntry from "./CompetenceReviewQueueEntry";
import PullRequestReviewQueueEntry from "./PullRequestReviewQueueEntry";
import FilterByNamesFilters from "./FilterByNamesFilters";

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
    filterByNamesContainer: {
      margin: 0,
      width: "100%",
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

  const props = {
    filterIncludeTags,
    filterExcludeTags,
    filterIncludeFlavours,
    filterExcludeFlavours,
    handleChangeFlavourFilter,
    handleChangeTagFilter,
    allTagNames,
    allFlavours,
    allTeamNames,
    filterIncludeAssigneeTeams,
    handleChangeAssigneeTeamFilter,
  };

  return (
    <Grid container spacing={3} className={classes.mainSection}>
      <Grid item xs={2} className={classes.filterByNamesContainer}>
        <FilterByNamesFilters {...props} />
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
              .map((project, index) => (
                <CompetenceReviewQueueEntry
                  project={project}
                  key={`${project}_${index}`}
                />
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
          </Grid>
          <Grid>
            {pullRequestReviewQueueProjects
              .filter(applyFilters)
              .sort(
                (a, b) =>
                  new Date(b.oldestOpenPrUpdatedTime) -
                  new Date(a.oldestOpenPrUpdatedTime)
              )
              .map((project, index) => (
                <PullRequestReviewQueueEntry
                  project={project}
                  key={`${project}_${index}`}
                />
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
