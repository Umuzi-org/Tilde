import React, { useEffect, useState } from "react";
import Presentation from "./Presentation";
import { showButtons, getTeamPermissions } from "./utils";
import { connect } from "react-redux";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";
import { addCardReviewOperations } from "../AddCardReviewModal/redux";

import { apiReduxApps } from "../../../apiAccess/apiApps";
import { MANAGE_CARDS } from "../../../constants";

function AgileCardActionsUnconnected({
  card,
  variant,
  viewedUser,

  // mapDispatchToProps
  startProject,
  requestReview,
  cancelReviewRequest,
  startTopic,
  stopTopic,
  finishTopic,
  openReviewFormModal,
  fetchcardsNeedingCompetenceReview,

  // mapStateToProps
  authUser,
  CARD_START_PROJECT,
  CARD_REQUEST_REVIEW,
  CARD_CANCEL_REVIEW_REQUEST,
  CARD_START_TOPIC,
  CARD_STOP_TOPIC,
  CARD_FINISH_TOPIC,
  cardsNeedingCompetenceReview,
  FETCH_COMPETENCE_REVIEWS_OUTSTANDING_FOR_USER,

  //storybook
  forceUser,
}) {
  const [
    outstandingReviewsModalOpen,
    setOutstandingReviewsModalOpen,
  ] = useState(false);

  const permissions = getTeamPermissions({ authUser, viewedUser });
  const canManageCards = permissions[MANAGE_CARDS];

  cardsNeedingCompetenceReview = Object.values(
    cardsNeedingCompetenceReview || {}
  ).filter((o) => o.reviewers.includes(viewedUser.id));

  const noReviewsOwed = cardsNeedingCompetenceReview.length === 0;
  useEffect(() => fetchcardsNeedingCompetenceReview({ user: viewedUser.id }), [
    fetchcardsNeedingCompetenceReview,
    viewedUser,
  ]);

  const cardId = card.id;
  variant = variant || "card";

  function openOutstandingReviewsModal() {
    setOutstandingReviewsModalOpen(true);
  }

  function handleCloseOutstandingReviewsModal() {
    setOutstandingReviewsModalOpen(false);
  }

  const handleStartTopic = () => {
    if (canManageCards || noReviewsOwed) {
      startTopic({ cardId });
    } else {
      openOutstandingReviewsModal();
    }
  };

  const handleStopTopic = () => {
    stopTopic({ cardId });
  };

  const handleFinishTopic = () => {
    if (canManageCards || noReviewsOwed) {
      finishTopic({ cardId });
    } else {
      openOutstandingReviewsModal();
    }
  };

  const handleClickAddReview = () => {
    openReviewFormModal({ cardId });
  };

  const handleRequestReview = () => {
    if (canManageCards || noReviewsOwed) {
      requestReview({ cardId });
    } else {
      openOutstandingReviewsModal();
    }
  };

  const handleStartProject = () => {
    if (canManageCards || noReviewsOwed) {
      startProject({ cardId });
    } else {
      openOutstandingReviewsModal();
    }
  };

  const handleCancelReviewRequest = () => {
    cancelReviewRequest({ cardId });
  };

  const loadingGetOutstandingCompetenceReviews = (getLatestMatchingCall({
    callLog: FETCH_COMPETENCE_REVIEWS_OUTSTANDING_FOR_USER,
    requestData: { user: viewedUser.id },
  }) || { loading: false })["loading"];

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

  authUser = forceUser || authUser;

  const props = {
    outstandingReviewsModalOpen,
    handleCloseOutstandingReviewsModal,
    cardsNeedingCompetenceReview,

    card,
    variant,
    authUser,
    ...showButtons({
      card,
      authUser,
      viewedUser,
    }),
    handleClickAddReview,
    handleRequestReview,
    handleStartProject,
    handleCancelReviewRequest,
    handleStartTopic,
    handleStopTopic,
    handleFinishTopic,

    loadingGetOutstandingCompetenceReviews,
    loadingStartProject,
    loadingStartTopic,
    loadingRequestReview,
    loadingCancelReviewRequest,
    loadingStopTopic,
    loadingFinishTopic,
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
    FETCH_COMPETENCE_REVIEWS_OUTSTANDING_FOR_USER:
      state.FETCH_COMPETENCE_REVIEWS_OUTSTANDING_FOR_USER,
    cardsNeedingCompetenceReview:
      state.apiEntities.cardsNeedingCompetenceReview,
    // CARD_REMOVE_WORKSHOP_ATTENDANCE: state.CARD_REMOVE_WORKSHOP_ATTENDANCE,
    // CARD_ADD_WORKSHOP_ATTENDANCE: state.CARD_ADD_WORKSHOP_ATTENDANCE,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
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

    fetchcardsNeedingCompetenceReview: ({ user }) => {
      dispatch(
        apiReduxApps.FETCH_COMPETENCE_REVIEWS_OUTSTANDING_FOR_USER.operations.maybeStart(
          { data: { user } }
        )
      );
    },

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
  };
};

const AgileCardActions = connect(
  mapStateToProps,
  mapDispatchToProps
)(AgileCardActionsUnconnected);

export default AgileCardActions;
