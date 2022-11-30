import React from "react";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import IconButton from "@material-ui/core/IconButton";
import CardBadges from "../../widgets/CardBadges";
import MoreIcon from "@material-ui/icons/More";
import { makeStyles } from "@material-ui/core/styles";
import TagChips from "../../widgets/TagChips";
import FlavourChips from "../../widgets/FlavourChips";
import { routes } from "../../../routes";
import AssigneesList from "../../widgets/AssigneesList";
import ReviewersTable from "../../widgets/ReviewersTable";

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

export default function BaseReviewQueueEntry({
  project,
  showAllocatedReviewers,
  reviewers,
}) {
  const classes = useStyles();
  // console.log("reviewers", reviewers ? reviewers : []);

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
            usersThatReviewedSinceLastReviewRequest={reviewers}
            usersThatReviewedSinceLastReviewRequestEmails={reviewers}
          />
        </React.Fragment>
      )}
    </Paper>
  );
}
