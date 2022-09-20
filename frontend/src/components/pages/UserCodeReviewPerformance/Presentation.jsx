import React from "react";
import {
  Grid,
  Paper,
  Typography,
  TableBody,
  Table,
  TableRow,
  TableCell,
  Avatar,
  Tooltip,
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

const useStyles = makeStyles((theme) => {
  const avatar = {
    float: "left",
    marginRight: theme.spacing(1),
    width: theme.spacing(5),
    height: theme.spacing(3),
    fontSize: theme.spacing(2),
    cursor: "pointer",
  };
  const result = { avatar };

  Object.keys(REVIEW_VALIDATED_STATUS_CHOICES).forEach((key) => {
    console.log(key);
    result[key] = {
      ...avatar,
      backgroundColor: reviewValidatedColors[key],
    };
  });

  return result;
});

function formatTime(timestamp) {
  const date = new Date(Date.parse(timestamp));
  return new Intl.DateTimeFormat().format(date);
}

function Presentation({ reviews }) {
  const classes = useStyles();

  reviews = reviews || [];

  const grouped = {};

  for (let review of reviews) {
    const { contentItem, flavourNames, title, contentItemAgileWeight } = review;

    const key = JSON.stringify({
      contentItem,
      flavourNames,
      title,
      contentItemAgileWeight,
    });
    grouped[key] = grouped[key] || [];
    grouped[key].push(review);
  }

  function getClassName({ review }) {
    if (review.validated !== null) {
      return classes[review.validated];
    }
    return classes.avatar;
  }

  return (
    <Grid container spacing={3}>
      <Grid item sx={4}>
        <Typography variant="h6">Competence Reviews</Typography>
        <Paper>
          <Table size="small">
            <TableBody>
              {Object.keys(grouped)
                .sort((a, b) => {
                  const weightA = JSON.parse(a).contentItemAgileWeight;
                  const weightB = JSON.parse(b).contentItemAgileWeight;
                  return weightB - weightA;
                })
                .map((key) => {
                  const {
                    contentItem,
                    flavourNames,
                    title,
                    contentItemAgileWeight,
                  } = JSON.parse(key);
                  const reviews = grouped[key];
                  return (
                    <TableRow key={key}>
                      <TableCell>
                        {title}
                        <FlavourChips
                          flavourNames={flavourNames}
                          variant="small"
                        />
                        <StoryPoints
                          storyPoints={contentItemAgileWeight}
                          variant="small"
                        />
                      </TableCell>

                      <TableCell>
                        {reviews
                          .sort(
                            (a, b) =>
                              new Date(a.timestamp) - new Date(b.timestamp)
                          )
                          .map((review) => (
                            <Link
                              to={routes.cardDetails.route.path.replace(
                                ":cardId",
                                review.agileCard
                              )}
                            >
                              <Tooltip
                                title={
                                  <React.Fragment>
                                    <Typography>
                                      {REVIEW_STATUS_CHOICES[review.status]}
                                    </Typography>
                                    <em>Timestamp:</em>{" "}
                                    {formatTime(review.timestamp)}
                                    <br />
                                    <em>Validated:</em>{" "}
                                    <span
                                      style={{
                                        color:
                                          reviewValidatedColors[
                                            review.validated
                                          ],
                                      }}
                                    >
                                      {
                                        REVIEW_VALIDATED_STATUS_CHOICES[
                                          review.validated
                                        ]
                                      }
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
                                >
                                  {review.status}
                                </Avatar>
                              </Tooltip>
                            </Link>
                          ))}
                      </TableCell>
                    </TableRow>
                  );
                })}
            </TableBody>
          </Table>
        </Paper>
      </Grid>
    </Grid>
  );
}

export default Presentation;
