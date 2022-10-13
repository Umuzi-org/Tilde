import React from "react";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/core/styles";
import Button from "../../widgets/Button";
import Loading from "../../widgets/Loading";
import CompetenceReviewQueueEntry from "./CompetenceReviewQueueEntry";
import PullRequestReviewQueueEntry from "./PullRequestReviewQueueEntry";
import FilterByNames from "./FilterByNames";
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
    },
    queueContainerHeadingFilters: {
      display: "flex",
      alignItems: "center",
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
}) {
  const classes = useStyles();

  filterIncludeTags = filterIncludeTags || [];
  filterExcludeTags = filterExcludeTags || [];
  filterIncludeFlavours = filterIncludeFlavours || [];
  filterExcludeFlavours = filterExcludeFlavours || [];

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
                <CompetenceReviewQueueEntry
                  project={project}
                  key={`${project.id}`}
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
                <PullRequestReviewQueueEntry
                  project={project}
                  key={`${project.id}`}
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
