import React from "react";

import Markdown from "react-markdown";
import Modal from "../../widgets/Modal";
import Card from "@material-ui/core/Card";
import Divider from "@material-ui/core/Divider";
import CloseIcon from "@material-ui/icons/Close";
import { makeStyles } from "@material-ui/core/styles";
import ReviewStatus from "../../widgets/ReviewStatus";
import {
  Button,
  CardContent,
  CardHeader,
  Typography,
} from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  cardStyle: {
    diplay: "block",
    height: "90vh",
    width: "90vw",
    overflow: "scroll",
    position: "relative",
    maxWidth: "90%",
  },
  cardContentStyle: {
    maxWidth: "90%",
  },
  exitIcon: {
    position: "absolute",
    top: "25px",
    right: "10px",
    backgroundColor: "white",
    "&:hover": {
      backgroundColor: "white"
    }
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
            <Button className={classes.exitIcon} onClick={closeModal}>
              <CloseIcon fontSize="large" />
            </Button>

            <CardHeader
              title={
                <Typography className={classes.timefont}>
                  Date: {timestamp.toLocaleDateString()}
                </Typography>
              }
              subheader={
                <Typography>
                  <div className={classes.reviewerEmailStyle}> 
                  Reviewer: {review.reviewerUserEmail} 
                  </div>
                  <div className={classes.reviewerEmailStyle}>
                    Status: <ReviewStatus status={review.status}/>
                  </div>
                </Typography>
              }
            />

            <Divider variant="middle"/>

            <div className={classes.reviewStyle}>
              <Typography>
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
