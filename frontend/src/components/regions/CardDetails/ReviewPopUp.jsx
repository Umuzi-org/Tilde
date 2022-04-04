import React from "react";

import Markdown from "react-markdown";
import Box from "@material-ui/core/Box";
import Modal from "../../widgets/Modal";
import Card from "@material-ui/core/Card";
import { makeStyles } from "@material-ui/core/styles";
import ReviewStatus from "../../widgets/ReviewStatus";
import { CardActions, CardContent, Typography } from "@material-ui/core";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";

const useStyles = makeStyles((theme) => ({
  cardStyle: {
    display: "block",
    position: "relative",
    maxWidth: "90%",
  },
  timeStyle: {
    fontSize: 11,
  },
  reviewerEmailStyle: {
    fontSize: "100%",
    fontWeight: "bold",
  },
  CardContent: {
    fontSize: "11px",
    padding: "20px",
    paddingRight: "30px",
    overflowY: "scroll",
    overflowX: "hidden",
    maxHeight: "50vh",
  },
  reviewCommentsPosition: {
    paddingLeft: "30px",
  },
}));

function ReviewPopUp({ review, openReviewPopUp, onClose }) {
  const classes = useStyles();
  const timestamp = new Date(review.timestamp);

  return (
    <Modal open={openReviewPopUp} onClose={onClose}>
      <Card className={classes.cardStyle}>
        <Box clone pt={2} pr={1} pb={1} pl={2}>
          <Paper elevation={3}>
            <div>
              <Grid container spacing={2} alignItems="center" wrap="nowrap">
                <Grid item>
                  <Typography>
                    <span>
                      {" "}
                      <Typography className={classes.timeStyle}>
                        Date:{" "}
                        {timestamp.toLocaleDateString() +
                          " " +
                          timestamp.toLocaleTimeString()}
                      </Typography>
                    </span>
                    <div className={classes.reviewerEmailStyle}>
                      {review.reviewerUserEmail}
                    </div>
                  </Typography>
                </Grid>
              </Grid>
            </div>
          </Paper>
        </Box>
        <Box>
          <CardContent
            className={classes.CardContent}
            children={
              <Typography className={classes.reviewCommentsPosition}>
                <Markdown children={review.comments} />
              </Typography>
            }
          />
        </Box>
        <CardActions>
          <ReviewStatus status={review.status} />
        </CardActions>
      </Card>
    </Modal>
  );
}

export default ReviewPopUp;
