import React from "react";
import {
  Paper,
  Typography,
  TableBody,
  Table,
  TableRow,
  TableCell,
  Avatar,
  Tooltip,
  TableHead,
  Chip,
} from "@material-ui/core";
import FlavourChips from "../../widgets/FlavourChips";
import StoryPoints from "../../widgets/StoryPoints";
import {
  REVIEW_VALIDATED_STATUS_CHOICES,
  REVIEW_STATUS_CHOICES,
} from "../../../constants";

import { routes } from "../../../routes";
import { Link } from "react-router-dom";

import { reviewValidatedColors, trustedColor } from "../../../colors";

import { makeStyles } from "@material-ui/core/styles";
import IconButton from "@material-ui/core/IconButton";
import ArrowRightIcon from "@material-ui/icons/ArrowRight";
import ArrowLeftIcon from "@material-ui/icons/ArrowLeft";

const COMPETENCE_REVIEW = "competence";
const PR_REVIEW = "pr";

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

  const result = { avatar, prAvatar };

  Object.keys(REVIEW_VALIDATED_STATUS_CHOICES).forEach((key) => {
    console.log(key);
    result[key] = {
      ...avatar,
      backgroundColor: reviewValidatedColors[key],
    };
  });

  return result;
});

function formatTimeString(timestamp) {
  const date = new Date(Date.parse(timestamp));
  return new Intl.DateTimeFormat().format(date);
}

function PullRequestReview({ review }) {
  const classes = useStyles();
  return (
    <Tooltip
      title={
        <React.Fragment>
          <Typography>{review.state}</Typography>
          <em>Timestamp:</em> {formatTimeString(review.timestamp)}
        </React.Fragment>
      }
    >
      <Avatar variant="rounded" className={classes.prAvatar}>
        PR {review.state}
      </Avatar>
    </Tooltip>
  );
}

function CompetenceReview({ review }) {
  const classes = useStyles();

  function getClassName({ review }) {
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
          <br />
          <em>Validated:</em>{" "}
          <span
            style={{
              color: reviewValidatedColors[review.validated],
            }}
          >
            {REVIEW_VALIDATED_STATUS_CHOICES[review.validated]}
          </span>
          <br />
          {review.trusted && (
            <span
              style={{
                color: trustedColor,
              }}
            >
              Trusted
            </span>
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

function Presentation({
  competenceReviews,
  pullRequestReviews,
  startDate,
  endDate,

  handleClickPrevious,
  handleClickNext,
}) {
  competenceReviews = competenceReviews || [];
  pullRequestReviews = pullRequestReviews || [];

  const grouped = {};

  for (let review of competenceReviews) {
    const { contentItem, flavourNames, title, contentItemAgileWeight } = review;

    const key = JSON.stringify({
      contentItem,
      flavourNames,
      title,
      contentItemAgileWeight,
    });
    grouped[key] = grouped[key] || [];
    grouped[key].push({ ...review, type: COMPETENCE_REVIEW });
  }

  for (let review of pullRequestReviews) {
    const { contentItem, flavourNames, title, contentItemAgileWeight } = review;

    const key = JSON.stringify({
      contentItem,
      flavourNames,
      title,
      contentItemAgileWeight,
    });
    grouped[key] = grouped[key] || [];
    grouped[key].push({
      ...review,
      type: PR_REVIEW,
      timestamp: review.submittedAt,
    });
  }

  return (
    <Paper>
      <IconButton aria-label="delete" size="big" onClick={handleClickPrevious}>
        <ArrowLeftIcon />
      </IconButton>
      {new Intl.DateTimeFormat().format(startDate)} -
      {new Intl.DateTimeFormat().format(endDate)}
      <IconButton aria-label="delete" size="big" onClick={handleClickNext}>
        <ArrowRightIcon />
      </IconButton>
      <Table size="small">
        {/* <TableHead>
          <TableRow>
            <TableCell></TableCell>
            <TableCell>competence reviews</TableCell>
            <TableCell>pr reviews</TableCell>
            <TableCell></TableCell>
          </TableRow>
        </TableHead> */}
        <TableBody>
          {Object.keys(grouped)
            .sort((a, b) => {
              const weightA = JSON.parse(a).contentItemAgileWeight;
              const weightB = JSON.parse(b).contentItemAgileWeight;
              return weightB - weightA;
            })
            .map((key) => {
              const {
                // contentItem,
                flavourNames,
                title,
                contentItemAgileWeight,
              } = JSON.parse(key);
              const reviews = grouped[key];
              return (
                <TableRow key={key}>
                  <TableCell>
                    {title}
                    <br />
                    <FlavourChips flavourNames={flavourNames} variant="small" />
                    <StoryPoints
                      storyPoints={contentItemAgileWeight}
                      variant="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={`Competence reviews ${
                        reviews.filter((r) => r.type === COMPETENCE_REVIEW)
                          .length
                      }`}
                    />
                    <Chip
                      label={`PR reviews ${
                        reviews.filter((r) => r.type === PR_REVIEW).length
                      }`}
                    />
                  </TableCell>

                  <TableCell>
                    {reviews
                      .sort(
                        (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
                      )
                      .map((review) => (
                        <Link
                          to={routes.cardDetails.route.path.replace(
                            ":cardId",
                            review.agileCard
                          )}
                        >
                          {review.type === COMPETENCE_REVIEW && (
                            <CompetenceReview review={review} />
                          )}

                          {review.type === PR_REVIEW && (
                            <PullRequestReview review={review} />
                          )}
                        </Link>
                      ))}
                  </TableCell>
                </TableRow>
              );
            })}
        </TableBody>
      </Table>
    </Paper>
  );
}

export default Presentation;
