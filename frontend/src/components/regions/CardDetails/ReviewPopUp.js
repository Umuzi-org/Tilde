import React from "react";

// import Typography from "@material-ui/core/Typography"
import Markdown from "react-markdown";
import Modal from "../../widgets/Modal";
import Card from "@material-ui/core/Card"
import { Button, CardContent, Typography } from "@material-ui/core";
import CloseIcon from "@material-ui/icons/Close"
import { sizing } from "@material-ui/system"

const ReviewPopUp = ({ review, openReviewPopUp, setOpenReviewPopUp }) => {

  return (
    <Modal
      open={openReviewPopUp}
      onClose={() => {
        setOpenReviewPopUp(false);
      }}
    >
      <Card
        style={{
          display: "flex",
          height: "90vh",
          width: "90vw",
          position: "relative",
          // maxWidth: "90%"
        }}

      >
        <CardContent>
          <div style={{
            // color: "blue"
          }}
          >
            <Button
              style={{
                position: "absolute",
                top: "5px",
                right: "1px"
              }}
              onClick={() => setOpenReviewPopUp(false)}>
              <CloseIcon fontSize="small" />
            </Button>
            <Typography
              style={
                {
                  fontSize: "100%",
                  fontWeight: "bold",
                }
              }
            >
              {review.reviewerUserEmail}'s review:⤵
            </Typography>
            <Typography
              style={{
                maxWidth: "90%"
              }}
            >
            <Markdown children={`${review.comments.split("\n")}`}
              style={{
                maxWidth: "90%"
              }}
            />
            </Typography>
            
          </div>
        </CardContent>
      </Card>

    </Modal>
  );
};

export default ReviewPopUp;
