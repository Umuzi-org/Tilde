import { Grid, Paper, Typography, IconButton } from "@material-ui/core";
import React from "react";

import CardBadges from "../../widgets/CardBadges";
import MoreIcon from "@material-ui/icons/More";
import { makeStyles } from "@material-ui/core/styles";
// import TagChips from "../../widgets/TagChips";
import FlavourChips from "../../widgets/FlavourChips";
import { routes } from "../../../routes";
import Button from "../../widgets/Button";
import AssigneesList from "../../widgets/AssigneesList";
import ReviewersTable from "../../widgets/ReviewersTable";
import Loading from "../../widgets/Loading";

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

      {/* <TagChips tagNames={project.tagNames} /> */}

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

function Presentation({
  competenceReviewQueueProjects,
  pullRequestReviewQueueProjects,

  competenceReviewQueueLoading,
  pullRequestReviewQueueLoading,

  fetchNextCompetenceReviewQueuePage,
  fetchNextPullRequestQueuePage,
}) {
  const classes = useStyles();
  return (
    <Grid container spacing={3}>
      <Grid item sx={6}>
        <Paper className={classes.queue} elevation={2}>
          {/* TODO center headings*/}
          <Typography variant="h5">Competence Review Queue</Typography>
          {/* TODO improve scrolling behavior: keep the heading in view, just scroll the items */}

          {competenceReviewQueueProjects.map((project) => (
            <CompetenceReviewQueueEntry project={project} />
          ))}

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
        </Paper>
      </Grid>
      <Grid item sx={6}>
        <Paper className={classes.queue} elevation={2}>
          <Typography variant="h5">Pull Request Review Queue</Typography>
          {/* TODO improve scrolling behavior: keep the heading in view, just scroll the items */}

          {pullRequestReviewQueueProjects.map((project) => (
            <PullRequestReviewQueueEntry project={project} />
          ))}

          <Paper elevation={3} className={classes.project} variant="outlined">
            {pullRequestReviewQueueLoading ? (
              <Loading />
            ) : (
              <Button onClick={fetchNextPullRequestQueuePage}>Load more</Button>
            )}
            {/* TODO Center the button or spinner*/}
          </Paper>
        </Paper>
      </Grid>
    </Grid>
  );
}

export default Presentation;