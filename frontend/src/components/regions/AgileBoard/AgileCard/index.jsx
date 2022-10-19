import React from "react";

import { showButtons } from "../../../../utils/cardButtons";
import Presentation from "./Presentation";

export default function AgileCardUnconnected({
  card,
  repoUrl,
  authUser,
  viewedUser,
  filterUserId,
  handleClickAddReview,

  handleRequestReview,
  handleStartProject,
  handleCancelReviewRequest,

  handleClickOpenWorkshopAttendanceForm,
  handleStartTopic,
  handleStopTopic,
  handleFinishTopic,
  handleRemoveWorkshopAttendance,

  loadingStartProject,
  loadingStartTopic,
  loadingClickOpenWorkshopAttendanceForm,
  loadingRequestReview,
  loadingCancelReviewRequest,
  loadingStopTopic,
  loadingFinishTopic,
  loadingRemoveWorkshopAttendance,
}) {
  const props = {
    card,
    // ...showButtons({
    //   card,
    //   authUser,
    //   viewedUser,
    // }),
    handleClickAddReview,

    repoUrl,
    authUser,
    viewedUser,
    filterUserId,
    handleRequestReview,
    handleStartProject,
    handleCancelReviewRequest,

    handleClickOpenWorkshopAttendanceForm,
    handleStartTopic,
    handleStopTopic,
    handleFinishTopic,
    handleRemoveWorkshopAttendance,
    loadingStartProject,
    loadingStartTopic,
    loadingClickOpenWorkshopAttendanceForm,
    loadingRequestReview,
    loadingCancelReviewRequest,
    loadingStopTopic,
    loadingFinishTopic,
    loadingRemoveWorkshopAttendance,
  };

  return <Presentation {...props} />;
}
