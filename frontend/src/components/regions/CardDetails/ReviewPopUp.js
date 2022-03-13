import React from "react";

import Markdown from "react-markdown";
import Box from "@material-ui/core/Box";
import Modal from "../../widgets/Modal";
import Card from "@material-ui/core/Card";
import CloseIcon from "@material-ui/icons/Close";
import { makeStyles } from "@material-ui/core/styles";
import ReviewStatus from "../../widgets/ReviewStatus";
import {
  Button,
  CardActions,
  CardContent,
  Typography,
} from "@material-ui/core";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";

const useStyles = makeStyles((theme) => ({
  cardStyle: {
    display: "block",
    position: "relative",
    maxWidth: "90%",
  },
  exitIcon: {
    position: "absolute",
    top: "5px",
    right: "5px",
    backgroundColor: "white",
    "&:hover": {
      backgroundColor: "white",
    },
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
    height: "66vh",
  },
  reviewCommentsPosition: {
    paddingLeft: "30px",
  },
}));

const ReviewPopUp = ({ review, openReviewPopUp, setOpenReviewPopUp }) => {
  const classes = useStyles();
  const closeModal = () => setOpenReviewPopUp(false);

  const timestamp = new Date(review.timestamp);

  return (
    <Modal open={openReviewPopUp} onClose={closeModal}>
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
                        <Button
                          className={classes.exitIcon}
                          onClick={closeModal}
                        >
                          <CloseIcon fontSize="small" />
                        </Button>
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
        <CardActions style={{ backgroundColor: "gray" }}>
          <ReviewStatus status={review.status} />
        </CardActions>
      </Card>
    </Modal>
  );
};

export default ReviewPopUp;
