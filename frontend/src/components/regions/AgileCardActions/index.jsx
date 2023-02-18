import React, { useEffect, useState } from "react";
import Presentation from "./Presentation";
import { showButtons, getTeamPermissions } from "./utils";
import { connect } from "react-redux";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";
import { addCardReviewOperations } from "../AddCardReviewModal/redux";

import { apiReduxApps } from "../../../apiAccess/apiApps";
import { MANAGE_CARDS } from "../../../constants";
import { useApiCallbacks } from "../../../hooks";
// import { useApiCallbacks } from "../../../hooks";

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
  fetchCardsNeedingCompetenceReview,

  // mapStateToProps
  authUser,
  CARD_START_PROJECT,
  CARD_REQUEST_REVIEW,
  CARD_CANCEL_REVIEW_REQUEST,
  CARD_START_TOPIC,
  CARD_STOP_TOPIC,
  CARD_FINISH_TOPIC,
  // cardsNeedingCompetenceReview,
  FETCH_COMPETENCE_REVIEWS_OUTSTANDING_FOR_USER,

  //storybook
  forceUser,
}) {
  const [
    outstandingReviewsModalOpen,
    setOutstandingReviewsModalOpen,
  ] = useState(false);

  const [attemptedCardAction, setAttemptedCardAction] = useState(null);
  const [
    cardsNeedingCompetenceReview,
    setCardsNeedingCompetenceReview,
  ] = useState([]);

  const permissions = getTeamPermissions({ authUser, viewedUser });
  const canManageCards = permissions[MANAGE_CARDS];

  // cardsNeedingCompetenceReview = Object.values(
  //   cardsNeedingCompetenceReview || {}
  // ).filter((o) => o.reviewers.includes(viewedUser.id));

  const defaultLatestCall = { loading: false };

  const latestGetOutstandingCompetenceReviewsCall = getLatestMatchingCall({
    callLog: FETCH_COMPETENCE_REVIEWS_OUTSTANDING_FOR_USER,
    requestData: { user: viewedUser.id },
  });

  // useApiCallbacks({
  //   lastCallEntry: latestGetOutstandingCompetenceReviewsCall,
  //   successResponseCallback: takeActionOrOpenModal,
  // });

  useEffect(() => {
    if (!latestGetOutstandingCompetenceReviewsCall) return;
    if (attemptedCardAction === null) return;
    if (latestGetOutstandingCompetenceReviewsCall.loading) return;

    const { cardId, action } = attemptedCardAction;
    setAttemptedCardAction(null);

    console.log({
      latestGetOutstandingCompetenceReviewsCall,
      attemptedCardAction,
    });

    setCardsNeedingCompetenceReview(
      latestGetOutstandingCompetenceReviewsCall.responseData
    );

    if (latestGetOutstandingCompetenceReviewsCall.responseData.length) {
      openOutstandingReviewsModal();
      return;
    }

    ({
      startTopic,
      startProject,
      requestReview,
      finishTopic,
    }[action]({ cardId }));

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    latestGetOutstandingCompetenceReviewsCall,
    // attemptedCardAction,
    // cardsNeedingCompetenceReview,
    // finishTopic,
    // requestReview,
    // startProject,
    // startTopic,
  ]);

  const cardId = card.id;
  variant = variant || "card";

  function openOutstandingReviewsModal() {
    setOutstandingReviewsModalOpen(true);
  }

  function handleCloseOutstandingReviewsModal() {
    setOutstandingReviewsModalOpen(false);
  }

  function maybeTakeCardAction({ cardId, action }) {
    console.log("maybeTakeCardAction");
    setAttemptedCardAction({ cardId, action });
    fetchCardsNeedingCompetenceReview({ user: viewedUser.id });
  }

  const handleStartTopic = () => {
    if (canManageCards) {
      startTopic({ cardId });
    } else {
      maybeTakeCardAction({ cardId, action: "startTopic" });
    }
  };

  const handleStopTopic = () => {
    stopTopic({ cardId });
  };

  const handleFinishTopic = () => {
    if (canManageCards) {
      finishTopic({ cardId });
    } else {
      maybeTakeCardAction({ cardId, action: "finishTopic" });
    }
  };

  const handleClickAddReview = () => {
    openReviewFormModal({ cardId });
  };

  const handleRequestReview = () => {
    if (canManageCards) {
      requestReview({ cardId });
    } else {
      maybeTakeCardAction({ cardId, action: "requestReview" });
    }
  };

  const handleStartProject = () => {
    if (canManageCards) {
      startProject({ cardId });
    } else {
      maybeTakeCardAction({ cardId, action: "startProject" });
    }
  };

  const handleCancelReviewRequest = () => {
    cancelReviewRequest({ cardId });
  };

  const latestStartProjectCall =
    getLatestMatchingCall({
      callLog: CARD_START_PROJECT,
      requestData: { cardId },
    }) ||
    latestGetOutstandingCompetenceReviewsCall ||
    defaultLatestCall;

  const latestStartTopicCall =
    getLatestMatchingCall({
      callLog: CARD_START_TOPIC,
      requestData: { cardId },
    }) ||
    latestGetOutstandingCompetenceReviewsCall ||
    defaultLatestCall;

  const latestRequestReviewCall =
    getLatestMatchingCall({
      callLog: CARD_REQUEST_REVIEW,
      requestData: { cardId },
    }) ||
    latestGetOutstandingCompetenceReviewsCall ||
    defaultLatestCall;

  const latestFinishTopicCall =
    getLatestMatchingCall({
      callLog: CARD_FINISH_TOPIC,
      requestData: { cardId },
    }) ||
    latestGetOutstandingCompetenceReviewsCall ||
    defaultLatestCall;

  // const loadingGetOutstandingCompetenceReviews = latestGetOutstandingCompetenceReviewsCall["loading"];

  const loadingStartProject = latestStartProjectCall["loading"];
  const loadingStartTopic = latestStartTopicCall["loading"];
  const loadingRequestReview = latestRequestReviewCall["loading"];
  const loadingCancelReviewRequest = (getLatestMatchingCall({
    callLog: CARD_CANCEL_REVIEW_REQUEST,
    requestData: { cardId },
  }) || defaultLatestCall)["loading"];
  const loadingStopTopic = (getLatestMatchingCall({
    callLog: CARD_STOP_TOPIC,
    requestData: { cardId },
  }) || defaultLatestCall)["loading"];
  const loadingFinishTopic = latestFinishTopicCall["loading"];

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

    // loadingGetOutstandingCompetenceReviews,
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

    fetchCardsNeedingCompetenceReview: ({ user }) => {
      dispatch(
        apiReduxApps.FETCH_COMPETENCE_REVIEWS_OUTSTANDING_FOR_USER.operations.start(
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
