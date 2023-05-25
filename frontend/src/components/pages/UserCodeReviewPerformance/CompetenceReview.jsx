import React from "react";
import { Typography, Avatar, Tooltip } from "@material-ui/core";

import {
  REVIEW_VALIDATED_STATUS_CHOICES,
  COMPLETE_REVIEW_CYCLE_CHOICES,
  REVIEW_STATUS_CHOICES,
  REVIEW_STATUS_CHOICES_POSITIVE,
  REVIEW_STATUS_CHOICES_NEGATIVE,
} from "../../../constants";

import {
  reviewValidatedColors,
  trustedColor,
  completeReviewCycleColors,
} from "../../../colors";

import { makeStyles } from "@material-ui/core/styles";

import { formatTimeString } from "./utils";

const useStyles = makeStyles((theme) => {
  const avatar = {
    float: "left",
    marginRight: theme.spacing(1),
    width: theme.spacing(5),
    height: theme.spacing(3),
    fontSize: theme.spacing(2),
    cursor: "pointer",
  };

  const prAvatar = {
    float: "left",
    marginRight: theme.spacing(1),
    width: theme.spacing(18),
    height: theme.spacing(3),
    fontSize: theme.spacing(1.5),
    cursor: "pointer",
  };

  const result = {
    avatar,
    prAvatar,
    completeReviewCycleTrue: {
      ...avatar,
      backgroundColor: completeReviewCycleColors[true],
    },
    completeReviewCycleFalse: {
      ...avatar,
      backgroundColor: completeReviewCycleColors[false],
    },
  };

  Object.keys(REVIEW_VALIDATED_STATUS_CHOICES).forEach((key) => {
    result[key] = {
      ...avatar,
      backgroundColor: reviewValidatedColors[key],
    };
  });

  return result;
});

export default function CompetenceReview({ review }) {
  const classes = useStyles();

  function getClassName({ review }) {
    if (review.completeReviewCycle !== null) {
      return review.completeReviewCycle
        ? classes.completeReviewCycleTrue
        : classes.completeReviewCycleFalse;
    }

    if (review.validated !== null) {
      return classes[review.validated];
    }
    return classes.avatar;
  }

  const style = review.trusted ? { border: `3px solid ${trustedColor}` } : {};

  return (
    <Tooltip
      title={
        <React.Fragment>
          <Typography>{REVIEW_STATUS_CHOICES[review.status]}</Typography>
          <em>Timestamp:</em> {formatTimeString(review.timestamp)}
          {REVIEW_STATUS_CHOICES_POSITIVE.includes(review.status) && (
            <React.Fragment>
              <br />
              <em>Validated:</em>{" "}
              <span
                style={{
                  color: reviewValidatedColors[review.validated],
                }}
              >
                {REVIEW_VALIDATED_STATUS_CHOICES[review.validated]}
              </span>
            </React.Fragment>
          )}
          {REVIEW_STATUS_CHOICES_NEGATIVE.includes(review.status) && (
            <React.Fragment>
              <br />
              <em>feedback cycle:</em>
              <span
                style={{
                  color: completeReviewCycleColors[review.completeReviewCycle],
                }}
              >
                {COMPLETE_REVIEW_CYCLE_CHOICES[review.completeReviewCycle]}
              </span>
            </React.Fragment>
          )}
          {review.trusted && (
            <React.Fragment>
              <br />
              <span
                style={{
                  color: trustedColor,
                }}
              >
                Trusted
              </span>
            </React.Fragment>
          )}
        </React.Fragment>
      }
    >
      <Avatar
        className={getClassName({ review })}
        variant="rounded"
        style={style}
      >
        {review.status}
      </Avatar>
    </Tooltip>
  );
}
