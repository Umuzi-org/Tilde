import React from "react";
import Presentation from "./Presentation";
import { showButtons } from "./utils";

export default ({
  authUser,
  viewedUser,

  card,
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
}) => {
  const props = {
    card,
    ...showButtons({
      card,
      authUser,
      viewedUser,
    }),
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
  };
  return <Presentation {...props} />;
};
