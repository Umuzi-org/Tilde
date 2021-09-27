import React from "react";
import LaunchIcon from "@material-ui/icons/Launch";
import ReviewValidationIcons from "./ReviewValidationIcons";
import ReviewStatus from "./ReviewStatus";
import { routes } from "../../routes";

import {
  Typography,
  Card,
  CardContent,
  Tooltip,
  CardActions,
  Button,
} from "@material-ui/core";

import { makeStyles } from "@material-ui/core/styles";

const timestampToLocaleString = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString();
};

const shorten = (str) => {
  const max = 50;
  if (str.length > max) return str.slice(0, max) + "...";
  return str;
};
const useStyles = makeStyles((theme) => ({
  grow: { flexGrow: 1 },
  comments: {
    background: theme.palette.info.light,
    padding: theme.spacing(1),
  },
}));

const BaseActionCard = ({ action, children, footer }) => {
  return (
    <Card varient="outlined">
      <CardContent>
        <Typography>{timestampToLocaleString(action.timestamp)}</Typography>{" "}
        <Typography variant="h6" component="h2">
          {action.actionType}
        </Typography>
        <Typography>{action.title}</Typography>
        {children}
      </CardContent>
      {footer && <CardActions>{footer}</CardActions>}
    </Card>
  );
};

export const ActionCardCompleted = ({
  card,
  // handleClickOpenProjectDetails,
}) => {
  const footer = (
    <a href={routes.cardDetails.route.path.replace(":cardId", card.id)}>
      <Button
        variant="outlined"
        color="default"
        size="small"
        startIcon={<LaunchIcon />}
        // onClick={handleClickOpenProjectDetails}
      >
        View Project
      </Button>
    </a>
  );

  return <BaseActionCard action={card} footer={footer}></BaseActionCard>;
};

export const ActionReviewedCard = ({
  review,
  // handleClickOpenProjectDetails,
  showReviewer,
  showReviewed,
}) => {
  const classes = useStyles();

  const footer = (
    <React.Fragment>
      <a
        href={routes.cardDetails.route.path.replace(
          ":cardId",
          review.agileCard
        )}
      >
        <Button
          variant="outlined"
          color="default"
          size="small"
          startIcon={<LaunchIcon />}
          // onClick={handleClickOpenProjectDetails}
        >
          View Project
        </Button>
      </a>
      <div className={classes.grow} />
      <ReviewStatus status={review.status} />

      <ReviewValidationIcons review={review} />
    </React.Fragment>
  );

  return (
    <BaseActionCard action={review} footer={footer}>
      <Tooltip title={review.comments}>
        <div className={classes.comments}>
          <Typography>{shorten(review.comments)}</Typography>
        </div>
      </Tooltip>
      {showReviewer && (
        <Typography>Reviewer: {review.reviewerUserEmail}</Typography>
      )}
      {showReviewed && (
        <Typography>Assignee: {review.reviewedUserEmails.join(",")}</Typography>
      )}
    </BaseActionCard>
  );
};
