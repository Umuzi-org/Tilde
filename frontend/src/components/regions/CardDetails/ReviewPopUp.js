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
  CardActions,
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
    top: "5px",
    right: "1px",
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
  // footer: {
  //   position: "absolute",
  //   backgroundColor: "white",
  //   bottom: 0,
  //   left: 0,
  // },
  ReviewStatus: {
    position: "absolute",
    bottom: 0,
    left: 0
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
              <CloseIcon fontSize="small" />
            </Button>

            <CardHeader
              title={
                <Typography className={classes.timefont}>
                  {timestamp.toLocaleDateString()}
                </Typography>
              }
              subheader={
                <Typography className={classes.reviewerEmailStyle}>
                  {review.reviewerUserEmail} ⤵
                </Typography>
              }
            />

            <Divider variant="middle" />

            <div className={classes.reviewStyle}>
              <Typography>
                <Markdown children={review.comments} />
              </Typography>
            </div>
          </div>
        </CardContent>

        <div className={classes.footer}>
          <CardActions className={classes.ReviewStatus}>
            <ReviewStatus status={review.status} style={{position: "fixed"}}/>
          </CardActions>
        </div>
      </Card>
    </Modal>
  );
};

export default ReviewPopUp;
