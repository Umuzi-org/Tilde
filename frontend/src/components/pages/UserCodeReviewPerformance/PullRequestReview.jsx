import React from "react";
import { Typography, Avatar, Tooltip } from "@material-ui/core";

import { makeStyles } from "@material-ui/core/styles";

import { formatTimeString } from "./utils";

import { REVIEW_VALIDATED_STATUS_CHOICES } from "../../../constants";

import { reviewValidatedColors } from "../../../colors";

import { ThemeProvider } from "@material-ui/styles";
import CssBaseline from "@material-ui/core/CssBaseline";
import theme from "../../widgets/theme";

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

  Object.keys(REVIEW_VALIDATED_STATUS_CHOICES).forEach((key) => {
    result[key] = {
      ...avatar,
      backgroundColor: reviewValidatedColors[key],
    };
  });

  return result;
});

export default function PullRequestReview({ review }) {
  const classes = useStyles();

  function getClassName({ review }) {
    if (review.validated === null || review.validated === undefined) {
      return classes.avatar;
    }
    return classes[review.validated];
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Tooltip
        title={
          <React.Fragment>
            <Typography>{review.state}</Typography>
            <em>Timestamp:</em> {formatTimeString(review.submittedAt)}
          </React.Fragment>
        }
      >
        <Avatar variant="rounded" className={getClassName({ review })}>
          PR {review.state}
        </Avatar>
      </Tooltip>
    </ThemeProvider>
  );
}
