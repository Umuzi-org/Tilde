import React, { useEffect } from "react";
import Presentation from "./Presentation";
import { showButtons } from "../../../../../utils/cardButtons";

import { useParams } from "react-router-dom";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../../../apiAccess/apiApps";

import { ACTION_NAMES } from "../../../../../constants";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";

function AgileCardUnconnected({
  authUser, // should only take in the authId
  viewedUser,

  // api calls
  requestReview,

  card,
  handleClickAddReview,
  handleClickOpenCardDetails,

  // handleRequestReview,
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
  useEffect(() => {
    requestReview({ cardId: card });
  }, [requestReview, card]);

  const handleRequestReview = () => {
    requestReview({ cardId: card });
  };

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

const mapStateToProps = (state) => {
  return {
    requestReview: state.apiEntities.requestReview,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    requestReview: ({ cardId }) => {
      dispatch(
        apiReduxApps.CARD_REQUEST_REVIEW.operations.start({
          data: { cardId },
        })
      );
    },
  };
};

const AgileCard = connect(
  mapStateToProps,
  mapDispatchToProps
)(AgileCardUnconnected);

export default AgileCard;
