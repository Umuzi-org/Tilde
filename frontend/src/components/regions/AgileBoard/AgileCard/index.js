import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { cardDetailsModalOperations } from "../../CardDetailsModal/redux";

import { addCardReviewOperations } from "../../AddCardReviewModal/redux";

// import { markSingleCardWorkshopAttendanceOperations } from "../../MarkSingleCardAttendanceModal/redux";

import { apiReduxApps } from "../../../../apiAccess/redux/apiApps";
import {
  READY,
  IN_PROGRESS,
  REVIEW_FEEDBACK,
  IN_REVIEW,
  COMPLETE,
  BLOCKED,
} from "../../../../constants";

export function showButtons({ card, authUser, startAllowed }) {
  const isReviewer = card.reviewers.indexOf(authUser.userId) !== -1;
  const isAssignee = card.assignees.indexOf(authUser.userId) !== -1;
  const isStaff = authUser.isStaff === 1;

  const showButtonStartProject =
    card.contentType === "project" &&
    ((startAllowed && isAssignee) ||
      (isStaff && [BLOCKED, READY].indexOf(card.status) !== -1));

  const showButtonRequestReview =
    isAssignee &&
    [IN_PROGRESS, REVIEW_FEEDBACK].indexOf(card.status) !== -1 &&
    (card.contentType === "project" || card.topicNeedsReview);
  const showButtonCancelReviewRequest =
    isAssignee && card.status === IN_REVIEW && card.contentType === "project";

  const showButtonAddReview =
    (isReviewer || isStaff) &&
    (card.contentType === "project" || card.topicNeedsReview) &&
    [IN_REVIEW, COMPLETE, REVIEW_FEEDBACK].indexOf(card.status) !== -1;

  // topic
  const showButtonStartTopic =
    startAllowed && isAssignee && card.contentType === "topic";
  const showButtonStopTopic =
    isAssignee && card.contentType === "topic" && card.status === IN_PROGRESS;
  const showButtonEndTopic = showButtonStopTopic;

  // workshop

  const showButtonNoteWorkshopAttendance =
    isStaff && card.contentType === "workshop" && card.status === READY;
  const showButtonCancelWorkshopAttendance =
    isStaff && card.contentType === "workshop" && card.status === COMPLETE;

  return {
    showButtonStartProject,
    showButtonRequestReview,
    showButtonCancelReviewRequest,
    showButtonAddReview,
    showButtonStartTopic,
    showButtonStopTopic,
    showButtonEndTopic,

    showButtonNoteWorkshopAttendance,
    showButtonCancelWorkshopAttendance,
  };
}

function AgileCardUnconnected({
  card,
  //   index,
  openCardDetailsModal,
  startProject,
  requestReview,
  cancelReviewRequest,
  //   openWorkshopAttendanceModal,
  startTopic,
  stopTopic,
  finishTopic,
  removeWorkshopAttendance,
  addWorkshopAttendance,
  authUser,
  openReviewFormModal,
  startAllowed, // according to the greater scheme of things, should starting work on this be allowed
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
    filterUserId,
    handleRequestReview,
    handleStartProject,
    handleCancelReviewRequest,

    handleClickOpenWorkshopAttendanceForm,
    handleStartTopic,
    handleStopTopic,
    handleFinishTopic,
    handleRemoveWorkshopAttendance,

    ...showButtons({ startAllowed, card, authUser }),
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
