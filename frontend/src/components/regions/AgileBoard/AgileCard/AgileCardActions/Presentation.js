import React from "react";
import Grid from "@material-ui/core/Grid";
import CardActions from "@material-ui/core/CardActions";
import MoreIcon from "@material-ui/icons/More";
import PlayCircleFilledWhiteIcon from "@material-ui/icons/PlayCircleFilledWhite";
import ArrowBackRoundedIcon from "@material-ui/icons/ArrowBackRounded";
import ArrowForwardRounded from "@material-ui/icons/ArrowForwardRounded";
import RateReviewRoundedIcon from "@material-ui/icons/RateReviewRounded";
import CardButton from "../../../../widgets/CardButton";
import ViewContentButton from "../../../../widgets/ViewContentButton";

export default ({
  card,

  handleClickOpenCardDetails,

  handleClickAddReview,
  handleRequestReview,
  handleStartProject,
  handleCancelReviewRequest,

  handleClickOpenWorkshopAttendanceForm,
  handleStartTopic,
  handleStopTopic,
  handleFinishTopic,
  handleRemoveWorkshopAttendance,

  showButtonStartProject,

  showButtonRequestReview,
  showButtonCancelReviewRequest,
  showButtonAddReview,
  showButtonStartTopic,
  showButtonStopTopic,
  showButtonEndTopic,
  showButtonNoteWorkshopAttendance,
  showButtonCancelWorkshopAttendance,
}) => {
  console.log({
    handleClickAddReview,
    handleClickOpenCardDetails,

    handleRequestReview,
    handleStartProject,
    handleCancelReviewRequest,

    handleClickOpenWorkshopAttendanceForm,
    handleStartTopic,
    handleStopTopic,
    handleFinishTopic,
    handleRemoveWorkshopAttendance,
  });
  return (
    <CardActions>
      <Grid container>
        <CardButton
          widget={
            <ViewContentButton
              contentUrl={card.contentItemUrl}
              contentItemId={card.contentItem}
            />
          }
        />

        {showButtonStartProject ? (
          <CardButton
            label="Start Project"
            startIcon={<PlayCircleFilledWhiteIcon />}
            onClick={handleStartProject}
          />
        ) : (
          ""
        )}

        <CardButton
          label="Details"
          startIcon={<MoreIcon />}
          onClick={handleClickOpenCardDetails}
        />

        {showButtonRequestReview ? (
          <CardButton
            label="Request Review"
            startIcon={<ArrowForwardRounded />}
            onClick={handleRequestReview}
          />
        ) : (
          ""
        )}

        {showButtonCancelReviewRequest ? (
          <CardButton
            label="Cancel Review Request"
            startIcon={<ArrowBackRoundedIcon />}
            onClick={handleCancelReviewRequest}
          />
        ) : (
          ""
        )}

        {showButtonAddReview ? (
          <CardButton
            label="Add Review"
            startIcon={<RateReviewRoundedIcon />}
            onClick={handleClickAddReview}
          />
        ) : (
          ""
        )}

        {showButtonStartTopic ? (
          <CardButton
            label="Start Topic"
            startIcon={<ArrowForwardRounded />}
            onClick={handleStartTopic}
          />
        ) : (
          ""
        )}

        {showButtonStopTopic ? (
          <CardButton
            label="Cancel"
            startIcon={<ArrowBackRoundedIcon />}
            onClick={handleStopTopic}
          />
        ) : (
          ""
        )}

        {showButtonEndTopic ? (
          <CardButton
            label="I'm done"
            startIcon={<ArrowForwardRounded />}
            onClick={handleFinishTopic}
          />
        ) : (
          ""
        )}

        {showButtonNoteWorkshopAttendance ? (
          <CardButton
            label="Mark Attendance"
            startIcon={<ArrowForwardRounded />}
            onClick={handleClickOpenWorkshopAttendanceForm}
          />
        ) : (
          ""
        )}

        {showButtonCancelWorkshopAttendance ? (
          <CardButton
            label="Cancel"
            startIcon={<ArrowBackRoundedIcon />}
            onClick={handleRemoveWorkshopAttendance}
          />
        ) : (
          ""
        )}
      </Grid>
    </CardActions>
  );
};
