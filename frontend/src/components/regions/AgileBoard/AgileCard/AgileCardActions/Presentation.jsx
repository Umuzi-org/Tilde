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

import { routes } from "../../../../../routes";

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

  loadingStartProject,
  loadingStartTopic,
  loadingClickOpenWorkshopAttendanceForm,
  loadingRequestReview,
  loadingCancelReviewRequest,
  loadingStopTopic,
  loadingFinishTopic,
  loadingRemoveWorkshopAttendance,
}) => {
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
            loading={loadingStartProject}
          />
        ) : (
          ""
        )}

        {/* <CardButton
            widget={<ViewCardDetailsButton cardId={card.Id}/>}
          /> */}

        <a href={routes.cardDetails.route.path.replace(":cardId", card.id)}>
          <CardButton label="Details" startIcon={<MoreIcon />} />{" "}
        </a>

        {/* <CardButton
          label="Details"
          startIcon={<MoreIcon />}
          onClick={handleClickOpenCardDetails}
        /> */}

        {showButtonRequestReview ? (
          <CardButton
            label="Request Review"
            startIcon={<ArrowForwardRounded />}
            onClick={handleRequestReview}
            loading={loadingRequestReview}
          />
        ) : (
          ""
        )}

        {showButtonCancelReviewRequest ? (
          <CardButton
            label="Cancel Review Request"
            startIcon={<ArrowBackRoundedIcon />}
            onClick={handleCancelReviewRequest}
            loading={loadingCancelReviewRequest}
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
            loading={loadingStartTopic}
          />
        ) : (
          ""
        )}

        {showButtonStopTopic ? (
          <CardButton
            label="Cancel"
            startIcon={<ArrowBackRoundedIcon />}
            onClick={handleStopTopic}
            loading={loadingStopTopic}
          />
        ) : (
          ""
        )}

        {showButtonEndTopic ? (
          <CardButton
            label="I'm done"
            startIcon={<ArrowForwardRounded />}
            onClick={handleFinishTopic}
            loading={loadingFinishTopic}
          />
        ) : (
          ""
        )}

        {showButtonNoteWorkshopAttendance ? (
          <CardButton
            label="Mark Attendance"
            startIcon={<ArrowForwardRounded />}
            onClick={handleClickOpenWorkshopAttendanceForm}
            loading={loadingClickOpenWorkshopAttendanceForm}
          />
        ) : (
          ""
        )}

        {showButtonCancelWorkshopAttendance ? (
          <CardButton
            label="Cancel"
            startIcon={<ArrowBackRoundedIcon />}
            onClick={handleRemoveWorkshopAttendance}
            loading={loadingRemoveWorkshopAttendance}
          />
        ) : (
          ""
        )}
      </Grid>
    </CardActions>
  );
};
