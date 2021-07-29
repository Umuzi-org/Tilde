import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { cardDetailsModalOperations } from "../../CardDetailsModal/redux";
import { getLatestMatchingCall } from "../../../../utils/ajaxRedux";
import { addCardReviewOperations } from "../../AddCardReviewModal/redux";

// import { markSingleCardWorkshopAttendanceOperations } from "../../MarkSingleCardAttendanceModal/redux";

import { apiReduxApps } from "../../../../apiAccess/redux/apiApps";

function AgileCardUnconnected({
  card,
  authUser,
  viewedUser,
  openCardDetailsModal,
  startProject,
  requestReview,
  cancelReviewRequest,
  startTopic,
  stopTopic,
  finishTopic,
  removeWorkshopAttendance,
  addWorkshopAttendance,
  openReviewFormModal,
  filterUserId,
  CARD_START_PROJECT,
  CARD_REQUEST_REVIEW,
  CARD_CANCEL_REVIEW_REQUEST,
  CARD_START_TOPIC,
  CARD_STOP_TOPIC,
  CARD_FINISH_TOPIC,
  CARD_REMOVE_WORKSHOP_ATTENDANCE,
  CARD_ADD_WORKSHOP_ATTENDANCE,
}) {
  const cardId = card.id;

  const handleClickOpenCardDetails = () => {
    openCardDetailsModal({ cardId });
  };

  const handleClickOpenWorkshopAttendanceForm = () => {
    // openWorkshopAttendanceModal({ cardId });
    addWorkshopAttendance({ cardId });
  };

  const handleStartTopic = () => {
    startTopic({ cardId });
  };

  const handleStopTopic = () => {
    stopTopic({ cardId });
  };

  const handleFinishTopic = () => {
    finishTopic({ cardId });
  };

  const handleRemoveWorkshopAttendance = () => {
    removeWorkshopAttendance({ cardId });
  };

  const handleClickAddReview = () => {
    openReviewFormModal({ cardId });
  };

  const handleRequestReview = () => {
    requestReview({ cardId });
  };

  const handleStartProject = () => {
    startProject({ cardId });
  };
  const handleCancelReviewRequest = () => {
    cancelReviewRequest({ cardId });
  };

  // due time button event - start
  const handleClickSetDueTime = () => {
    showAgileCardDueDateForm();
  }
  // due time button event - end

  const loadingStartProject = (getLatestMatchingCall({
    callLog: CARD_START_PROJECT,
    requestData: { cardId },
  }) || { loading: false })["loading"];
  const loadingStartTopic = (getLatestMatchingCall({
    callLog: CARD_START_TOPIC,
    requestData: { cardId },
  }) || { loading: false })["loading"];
  const loadingRequestReview = (getLatestMatchingCall({
    callLog: CARD_REQUEST_REVIEW,
    requestData: { cardId },
  }) || { loading: false })["loading"];
  const loadingCancelReviewRequest = (getLatestMatchingCall({
    callLog: CARD_CANCEL_REVIEW_REQUEST,
    requestData: { cardId },
  }) || { loading: false })["loading"];
  const loadingStopTopic = (getLatestMatchingCall({
    callLog: CARD_STOP_TOPIC,
    requestData: { cardId },
  }) || { loading: false })["loading"];
  const loadingFinishTopic = (getLatestMatchingCall({
    callLog: CARD_FINISH_TOPIC,
    requestData: { cardId },
  }) || { loading: false })["loading"];
  const loadingRemoveWorkshopAttendance = (getLatestMatchingCall({
    callLog: CARD_REMOVE_WORKSHOP_ATTENDANCE,
    requestData: { cardId },
  }) || { loading: false })["loading"];
  const loadingClickOpenWorkshopAttendanceForm = (getLatestMatchingCall({
    callLog: CARD_ADD_WORKSHOP_ATTENDANCE,
    requestData: { cardId },
  }) || { loading: false })["loading"];

  const props = {
    card,
    handleClickOpenCardDetails,
    handleClickAddReview,
    // due time button event - start
    handleClickSetDueTime,
    // due time button event - end

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

const mapStateToProps = (state) => {
  return {
    authUser: state.App.authUser,
    CARD_START_PROJECT: state.CARD_START_PROJECT,
    CARD_REQUEST_REVIEW: state.CARD_REQUEST_REVIEW,
    CARD_CANCEL_REVIEW_REQUEST: state.CARD_CANCEL_REVIEW_REQUEST,
    CARD_START_TOPIC: state.CARD_START_TOPIC,
    CARD_STOP_TOPIC: state.CARD_STOP_TOPIC,
    CARD_FINISH_TOPIC: state.CARD_FINISH_TOPIC,
    CARD_REMOVE_WORKSHOP_ATTENDANCE: state.CARD_REMOVE_WORKSHOP_ATTENDANCE,
    CARD_ADD_WORKSHOP_ATTENDANCE: state.CARD_ADD_WORKSHOP_ATTENDANCE,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    openCardDetailsModal: ({ cardId }) => {
      dispatch(cardDetailsModalOperations.openCardDetailsModal({ cardId }));
    },

    startProject: ({ cardId }) => {
      dispatch(
        apiReduxApps.CARD_START_PROJECT.operations.start({
          data: { cardId },
        })
      );
    },
    requestReview: ({ cardId }) => {
      dispatch(
        apiReduxApps.CARD_REQUEST_REVIEW.operations.start({
          data: { cardId },
        })
      );
    },
    cancelReviewRequest: ({ cardId }) => {
      dispatch(
        apiReduxApps.CARD_CANCEL_REVIEW_REQUEST.operations.start({
          data: {
            cardId,
          },
        })
      );
    },

    openReviewFormModal: ({ cardId }) => {
      dispatch(addCardReviewOperations.openCardReviewForm({ cardId }));
    },

    // openWorkshopAttendanceModal: ({ cardId }) => {
    //   dispatch(
    //     markSingleCardWorkshopAttendanceOperations.openWorkshopCardAttendanceForm(
    //       { cardId }
    //     )
    //   );
    // },

    startTopic: ({ cardId }) => {
      dispatch(
        apiReduxApps.CARD_START_TOPIC.operations.start({
          data: { cardId },
        })
      );
    },

    stopTopic: ({ cardId }) => {
      dispatch(
        apiReduxApps.CARD_STOP_TOPIC.operations.start({
          data: { cardId },
        })
      );
    },

    finishTopic: ({ cardId }) => {
      dispatch(
        apiReduxApps.CARD_FINISH_TOPIC.operations.start({
          data: { cardId },
        })
      );
    },

    removeWorkshopAttendance: ({ cardId }) => {
      dispatch(
        apiReduxApps.CARD_REMOVE_WORKSHOP_ATTENDANCE.operations.start({
          data: { cardId },
        })
      );
    },

    addWorkshopAttendance: ({ cardId }) => {
      dispatch(
        apiReduxApps.CARD_ADD_WORKSHOP_ATTENDANCE.operations.start({
          data: { cardId },
        })
      );
    },

    // due time button event - start
    showAgileCardDueDateForm: ({}) => {
      dispatch();
    },
    // due time button event - end
  };
};

const AgileCard = connect(
  mapStateToProps,
  mapDispatchToProps
)(AgileCardUnconnected);

export default AgileCard;
