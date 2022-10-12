import React, { useEffect, useState } from "react";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import TextField from "@material-ui/core/TextField";
import { makeStyles } from "@material-ui/core/styles";
import Button from "../../widgets/Button";
import Loading from "../../widgets/Loading";
import CompetenceReviewQueueEntry from "./CompetenceReviewQueueEntry";
import PullRequestReviewQueueEntry from "./PullRequestReviewQueueEntry";
import FilterByNames from "./FilterByNames";

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
    filterByNameTextField: {
      marginBottom: theme.spacing(2),
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
  filterIncludeCardNames,
  handleChangeCardNameFilter,
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

  const allCardNames = [
    ...new Set(
      [
        ...competenceReviewQueueProjects.map((proj) => proj.contentItemTitle),
        pullRequestReviewQueueProjects.map((proj) => proj.contentItemTitle),
      ]
        .flat()
        .flat() // yes, twice
    ),
  ];

  const [searchTerm, setSearchTerm] = useState("");
  const [allFoundCardNames, setAllFoundCardNames] = useState([]);

  function handleChangeSearchTerm(e) {
    setSearchTerm(e.target.value);
  }

  useEffect(() => {
    setAllFoundCardNames(() =>
      allCardNames.filter((cardName) =>
        cardName.toLocaleLowerCase().includes(searchTerm)
      )
    );
  }, [searchTerm, allCardNames]);

  function applyFilters(project) {
    if (filterIncludeTags.length) {
      for (let tag of filterIncludeTags) {
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

    if (filterIncludeCardNames.length) {
      for (const cardName of filterIncludeCardNames) {
        if (!project.contentItemTitle.includes(cardName)) return false;
      }
    }

    return true;
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

        <Typography variant="h6">Filter by card name</Typography>
        <Paper>
          <TextField
            className={classes.filterByNameTextField}
            variant="outlined"
            placeholder="Card name"
            value={searchTerm}
            onChange={handleChangeSearchTerm}
            fullWidth
          />
          <FilterByNames
            allNames={searchTerm ? allFoundCardNames : allCardNames}
            filterInclude={filterIncludeCardNames}
            filterExclude={[]}
            onChange={handleChangeCardNameFilter}
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
          </Grid>
          <Grid>
            {pullRequestReviewQueueProjects
              .filter(applyFilters)
              .sort(
                (a, b) =>
                  new Date(b.oldestOpenPrUpdatedTime) -
                  new Date(a.oldestOpenPrUpdatedTime)
              )
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
