import React from "react";

import Markdown from "react-markdown";
import Modal from "../../widgets/Modal";
import Card from "@material-ui/core/Card";
import Divider from "@material-ui/core/Divider";
import CloseIcon from "@material-ui/icons/Close";
import { makeStyles } from "@material-ui/core/styles";
import ReviewStatus from "../../widgets/ReviewStatus";
import { Button, CardContent, CardHeader, Typography } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  root: {
    position: "fixed",
    backgroundColor: "white",
    margin: "0px",
    width: "80%",
  },
  cardStyle: {
    diplay: "block",
    height: "90vh",
    width: "90vw",
    overflow: "scroll",
    position: "relative",
    maxWidth: "90%",
    overflowX: 'hidden'
  },
  cardContentStyle: {
    margin: 0,
    padding: 0,
    maxWidth: "90%",
  },
  exitIcon: {
    position: "absolute",
    top: "25px",
    right: "10px",
    backgroundColor: "white",
    "&:hover": {
      backgroundColor: "white",
    },
  },
  timefont: {
    fontSize: 11,
  },
  reviewerEmailStyle: {
    fontSize: "100%",
    fontWeight: "bold",
  },
  reviewStyle: {
    width: "100%",
    overflow: "hidden",
    padding: 10,
  },
  horizontalDivider: {
    paddingTop: "20px",
  },
  contentStart: {
    paddingTop: "110px"
  }
}));

const ReviewPopUp = ({ review, openReviewPopUp, setOpenReviewPopUp }) => {
  const classes = useStyles();
  const closeModal = () => setOpenReviewPopUp(false);

  const timestamp = new Date(review.timestamp);

  return (
    <Modal open={openReviewPopUp} onClose={closeModal}>
      <Card className={classes.cardStyle}>
        <CardContent className={classes.cardContentStyle}>
          <div>
            <CardHeader
              className={classes.root}
              title={
                <Typography className={classes.timefont}>
                  Date:{" "}
                  {timestamp.toLocaleDateString() +
                    " " +
                    timestamp.toLocaleTimeString()}
                  <Button className={classes.exitIcon} onClick={closeModal}>
                    <CloseIcon fontSize="medium" />
                  </Button>
                </Typography>
              }
              subheader={
                <Typography>
                  <div>
                    Reviewer:{" "}
                    <span className={classes.reviewerEmailStyle}>
                      {review.reviewerUserEmail}⤵
                    </span>
                  </div>
                  <div>
                    Status:{" "}
                    <span>
                      <ReviewStatus status={review.status} />
                    </span>
                    <div className={classes.horizontalDivider}>
                      <Divider variant="middle" />
                    </div>
                  </div>
                </Typography>
              }
            />

            <div className={classes.reviewStyle}>
              <Typography className={classes.contentStart}>
                <Markdown children={review.comments} />
              </Typography>
            </div>
          </div>
        </CardContent>
      </Card>
    </Modal>
  );
};

export default ReviewPopUp;
