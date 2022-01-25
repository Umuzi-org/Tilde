import React from "react";

import Typography from "@material-ui/core/Typography"
import Markdown from "react-markdown";
import Modal from "../../widgets/Modal";

const ReviewPopUp = ({ review, openReviewPopUp, setOpenReviewPopUp }) => {
  return (
    <Modal
      open={openReviewPopUp}
      onClose={() => {
        setOpenReviewPopUp(false);
      }}
    >
      <Typography variant="h6" component="div">
        {review.reviewerUserEmail}'s review:
      </Typography>
      <Markdown children={review.comments} />
    </Modal>
  );
};

export default ReviewPopUp;
