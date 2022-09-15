import {
  Grid,
  Paper,
  Typography,
  IconButton,
  FormGroup,
  FormControlLabel,
  Switch,
} from "@material-ui/core";
import React from "react";

import CardBadges from "../../widgets/CardBadges";
import MoreIcon from "@material-ui/icons/More";
import { makeStyles } from "@material-ui/core/styles";
import TagChips from "../../widgets/TagChips";
import FlavourChips from "../../widgets/FlavourChips";
import { routes } from "../../../routes";
import Button from "../../widgets/Button";
import AssigneesList from "../../widgets/AssigneesList";
import ReviewersTable from "../../widgets/ReviewersTable";
import Loading from "../../widgets/Loading";

// TODO: update files and code to match styleguide
// TODO: test solution with real data/ identical dummy data
// TODO: get rid of the overflow at the top when scrolling
const useStyles = makeStyles((theme) => {
  return {
    row: {
      padding: 5,
    },
    queue: {
      padding: theme.spacing(1),
    },
    project: {
      marginTop: theme.spacing(1),
      padding: theme.spacing(1),
    },
    left: {
      float: "left",
    },
    right: {
      // float: "right",
    },
    flexContainer: {
      display: "flex",
    },
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
    },
  };
});

// function TimesTable({ project }) {
//   const classes = useStyles();
//   const nice = (dateTime) => {
//     if (dateTime) {
//       const date = new Date(Date.parse(dateTime));
//       return new Intl.DateTimeFormat().format(date);
//     }
//   };

//   return (
//     <Table size="small">
//       <TableBody>
//         <TableRow className={classes.row}>
//           <TableCell>Start time</TableCell>
//           <TableCell>{nice(project.startTime)}</TableCell>
//         </TableRow>
//         <TableRow className={classes.row}>
//           <TableCell>Due time</TableCell>
//           <TableCell>{nice(project.dueTime)}</TableCell>
//         </TableRow>
//         <TableRow className={classes.row}>
//           <TableCell>Review Request time</TableCell>
//           <TableCell>{nice(project.reviewRequestTime)}</TableCell>
//         </TableRow>
//         <TableRow className={classes.row}>
//           <TableCell>Oldest PR update time</TableCell>
//           <TableCell>{nice(project.oldestOpenPrUpdatedTime)}</TableCell>
//         </TableRow>
//       </TableBody>
//     </Table>
//   );
// }

function BaseReviewQueueEntry({ project, showAllocatedReviewers }) {
  const classes = useStyles();
  return (
    <Paper elevation={3} className={classes.project} variant="outlined">
      <div className={classes.flexContainer}>
        {/* TODO: replace with a stack once MUI is upgraded */}
        <div className={classes.left}>
          <Typography>{project.contentItemTitle}</Typography>
        </div>
        <div className={classes.left}>
          <FlavourChips flavourNames={project.flavourNames} />
        </div>
        <div className={classes.left}>
          <CardBadges card={project} />
        </div>
        <div className={classes.right}>
          <a
            href={routes.cardDetails.route.path.replace(
              ":cardId",
              project.agileCard
            )}
          >
            <IconButton>
              <MoreIcon />
            </IconButton>
          </a>
        </div>
      </div>

      <TagChips tagNames={project.tagNames} />

      {/* <TimesTable project={project} /> */}

      <Typography>Assignees</Typography>
      <AssigneesList
        userIds={project.recruitUsers}
        userNames={project.recruitUserEmails}
      />

      {showAllocatedReviewers && (
        <React.Fragment>
          <Typography>Reviewers</Typography>
          <ReviewersTable
            reviewerUsers={project.reviewerUsers}
            reviewerUserEmails={project.reviewerUserEmails}
            usersThatReviewedSinceLastReviewRequest={
              project.usersThatReviewedSinceLastReviewRequest
            }
            usersThatReviewedSinceLastReviewRequestEmails={
              project.usersThatReviewedSinceLastReviewRequestEmails
            }
          />
        </React.Fragment>
      )}
    </Paper>
  );
}

function PullRequestReviewQueueEntry({ project }) {
  return BaseReviewQueueEntry({ project });
}

function CompetenceReviewQueueEntry({ project }) {
  return BaseReviewQueueEntry({ project, showAllocatedReviewers: true });
}

function FilterByNames({ allNames, filterInclude, filterExclude, onChange }) {
  const allFilters = [...filterInclude, ...filterExclude];

  return (
    <React.Fragment>
      {allNames.map((name) => (
        <FormGroup>
          <FormControlLabel
            control={
              <Switch
                size="small"
                color={filterExclude.includes(name) ? "secondary" : "primary"}
                onChange={onChange(name)}
              />
            }
            label={name}
            checked={allFilters.includes(name)}
          />
        </FormGroup>
      ))}
    </React.Fragment>
  );
}

function Presentation({
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

export default Presentation;
