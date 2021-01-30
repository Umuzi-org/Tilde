import React from "react";

import LaunchIcon from "@material-ui/icons/Launch";
import ReviewValidationIcons from "./ReviewValidationIcons";
import ReviewStatus from "./ReviewStatus";

import {
  Typography,
  Card,
  CardContent,
  Tooltip,
  CardActions,
  Button,
} from "@material-ui/core";

import { REVIEW_STATUS_CHOICES } from "../../constants";
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

export default ({
  review,
  handleClickOpenProjectDetails,
  showReviewer,
  showReviewed,
}) => {
  //   console.log(JSON.stringify(review));
  const classes = useStyles();
  //   const StatusIcon = statusIcons[review.status];

  return (
    <Card variant="outlined">
      <CardContent>
        <Typography>{timestampToLocaleString(review.timestamp)}</Typography>{" "}
        {/* <StatusIcon /> */}
        <Typography variant="h6" component="h2">
          Competence Review
        </Typography>
        <Typography>{review.title}</Typography>
        <Tooltip title={review.comments}>
          <div className={classes.comments}>
            <Typography>{shorten(review.comments)}</Typography>
          </div>
        </Tooltip>
        {showReviewer && (
          <Typography>Reviewer: {review.reviewerUserEmail}</Typography>
        )}
        {showReviewed && (
          <Typography>
            Assignee: {review.reviewedUserEmails.join(",")}
          </Typography>
        )}
      </CardContent>
      <CardActions>
        <Button
          variant="outlined"
          color="default"
          size="small"
          startIcon={<LaunchIcon />}
          onClick={handleClickOpenProjectDetails}
        >
          View Project
        </Button>
        <div className={classes.grow} />
        <ReviewStatus status={review.status} />

        <ReviewValidationIcons review={review} />
      </CardActions>
    </Card>
  );
};
