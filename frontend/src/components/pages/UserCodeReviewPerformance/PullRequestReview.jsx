import React from "react";
import { Typography, Avatar, Tooltip } from "@material-ui/core";

import { makeStyles } from "@material-ui/core/styles";

import { formatTimeString } from "./utils";

const useStyles = makeStyles((theme) => {
  const avatar = {
    float: "left",
    marginRight: theme.spacing(1),
    width: theme.spacing(18),
    height: theme.spacing(3),
    fontSize: theme.spacing(1.5),
    cursor: "pointer",
  };

  const result = {
    avatar,
  };

  return result;
});

export default function PullRequestReview({ review }) {
  const classes = useStyles();
  return (
    <Tooltip
      title={
        <React.Fragment>
          <Typography>{review.state}</Typography>
          <em>Timestamp:</em> {formatTimeString(review.submittedAt)}
        </React.Fragment>
      }
    >
      <Avatar variant="rounded" className={classes.avatar}>
        PR {review.state}
      </Avatar>
    </Tooltip>
  );
}
