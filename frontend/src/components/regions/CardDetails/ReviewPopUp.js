import React from "react";

import Markdown from "react-markdown";
import Modal from "../../widgets/Modal";
import Card from "@material-ui/core/Card"
import CloseIcon from "@material-ui/icons/Close"
import { Button, CardContent, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  cardStyle: {
    diplay: "block",
    height: "90vh",
    width: "90vw",
    overflow: "scroll",
    position: "relative",
    maxWidth: "90%"
  },
  cardContentStyle: {
    maxWidth: "90%",
  },
  exitIcon: {
    position: "absolute",
    top: "5px",
    right: "1px"
  },
  reviewerEmailStyle: {
    fontSize: "100%",
    fontWeight: "bold",
  }
}))

const ReviewPopUp = ({ review, openReviewPopUp, setOpenReviewPopUp }) => {

  const classes = useStyles()
  const closeModal = () => setOpenReviewPopUp(false)

  return (
    <Modal
      open={openReviewPopUp}
      onClose={closeModal}
    >
      <Card
        className={classes.cardStyle}
      >
        <CardContent
          className={classes.cardContentStyle}
        >
          <div>
            <Button
              className={classes.exitIcon}
              onClick={closeModal}>
              <CloseIcon fontSize="small" />
            </Button>
            <Typography
              className={classes.reviewerEmailStyle}
            >
              {review.reviewerUserEmail}'s review:⤵
            </Typography>
            <Typography>
              <Markdown children={review.comments}/>
            </Typography>

          </div>
        </CardContent>
      </Card>

    </Modal>
  );
};

export default ReviewPopUp;
