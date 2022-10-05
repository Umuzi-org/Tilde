import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";
import { addCardReviewOperations } from "../../AddCardReviewModal/redux";
import { apiReduxApps } from "../../../../apiAccess/apiApps";

export default function AgileCardUnconnected({
  card,
  repoUrl,
  authUser,
  viewedUser,
  filterUserId,
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

  loadingStartProject,
  loadingStartTopic,
  loadingClickOpenWorkshopAttendanceForm,
  loadingRequestReview,
  loadingCancelReviewRequest,
  loadingStopTopic,
  loadingFinishTopic,
  loadingRemoveWorkshopAttendance,
}) {
  // const cardId = card.id;

  // const handleClickOpenWorkshopAttendanceForm = () => {
  //   // openWorkshopAttendanceModal({ cardId });
  //   addWorkshopAttendance({ cardId });
  // };

  // const handleStartTopic = () => {
  //   startTopic({ cardId });
  // };

  // const handleStopTopic = () => {
  //   stopTopic({ cardId });
  // };

  // const handleFinishTopic = () => {
  //   finishTopic({ cardId });
  // };

  // const handleRemoveWorkshopAttendance = () => {
  //   removeWorkshopAttendance({ cardId });
  // };

  // const handleClickAddReview = () => {
  //   openReviewFormModal({ cardId });
  // };

  // const handleRequestReview = () => {
  //   requestReview({ cardId });
  // };

  // const handleStartProject = () => {
  //   startProject({ cardId });
  // };
  // const handleCancelReviewRequest = () => {
  //   cancelReviewRequest({ cardId });
  // };

  // const loadingStartProject = (getLatestMatchingCall({
  //   callLog: CARD_START_PROJECT,
  //   requestData: { cardId },
  // }) || { loading: false })["loading"];
  // const loadingStartTopic = (getLatestMatchingCall({
  //   callLog: CARD_START_TOPIC,
  //   requestData: { cardId },
  // }) || { loading: false })["loading"];
  // const loadingRequestReview = (getLatestMatchingCall({
  //   callLog: CARD_REQUEST_REVIEW,
  //   requestData: { cardId },
  // }) || { loading: false })["loading"];
  // const loadingCancelReviewRequest = (getLatestMatchingCall({
  //   callLog: CARD_CANCEL_REVIEW_REQUEST,
  //   requestData: { cardId },
  // }) || { loading: false })["loading"];
  // const loadingStopTopic = (getLatestMatchingCall({
  //   callLog: CARD_STOP_TOPIC,
  //   requestData: { cardId },
  // }) || { loading: false })["loading"];
  // const loadingFinishTopic = (getLatestMatchingCall({
  //   callLog: CARD_FINISH_TOPIC,
  //   requestData: { cardId },
  // }) || { loading: false })["loading"];
  // const loadingRemoveWorkshopAttendance = (getLatestMatchingCall({
  //   callLog: CARD_REMOVE_WORKSHOP_ATTENDANCE,
  //   requestData: { cardId },
  // }) || { loading: false })["loading"];
  // const loadingClickOpenWorkshopAttendanceForm = (getLatestMatchingCall({
  //   callLog: CARD_ADD_WORKSHOP_ATTENDANCE,
  //   requestData: { cardId },
  // }) || { loading: false })["loading"];

  const props = {
    card,

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
