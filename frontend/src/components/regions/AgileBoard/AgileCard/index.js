import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { cardDetailsModalOperations } from "../../CardDetailsModal/redux";

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
}) {
  const handleClickOpenCardDetails = () => {
    openCardDetailsModal({ cardId: card.id });
  };

  const handleClickOpenWorkshopAttendanceForm = () => {
    // openWorkshopAttendanceModal({ cardId: card.id });
    addWorkshopAttendance({ cardId: card.id });
  };

  const handleStartTopic = () => {
    startTopic({ cardId: card.id });
  };

  const handleStopTopic = () => {
    stopTopic({ cardId: card.id });
  };

  const handleFinishTopic = () => {
    finishTopic({ cardId: card.id });
  };

  const handleRemoveWorkshopAttendance = () => {
    removeWorkshopAttendance({ cardId: card.id });
  };

  const handleClickAddReview = () => {
    openReviewFormModal({ cardId: card.id });
  };

  const handleRequestReview = () => {
    requestReview({ cardId: card.id });
  };

  const handleStartProject = () => {
    startProject({ cardId: card.id });
  };
  const handleCancelReviewRequest = () => {
    cancelReviewRequest({ cardId: card.id });
  };

  const props = {
    card,
    handleClickOpenCardDetails,
    handleClickAddReview,

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
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    authUser: state.App.authUser,
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
  };
};

const AgileCard = connect(
  mapStateToProps,
  mapDispatchToProps
)(AgileCardUnconnected);

export default AgileCard;
