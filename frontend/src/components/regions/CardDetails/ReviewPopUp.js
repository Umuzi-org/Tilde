import React from "react";
import {
  Dialog,
  DialogContent,
  DialogTitle,
  Typography,
} from "@material-ui/core";

const ReviewPopUp = (props) => {
  const { title, children, openReviewPopUp, setOpenReviewPopUp } = props;
  return (
    <Dialog
      open={openReviewPopUp}
      onClose={() => {
        setOpenReviewPopUp(false);
      }}
    >
      <DialogTitle>
        <div>
          <Typography variant="h6" component="div">
            {title}
          </Typography>
        </div>
      </DialogTitle>
      <DialogContent dividers>
        <div>{children}</div>
      </DialogContent>
    </Dialog>
  );
};

export default ReviewPopUp;
