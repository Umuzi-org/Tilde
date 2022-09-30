import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../apiAccess/apiApps";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";
import operations from "./redux/operations.js";
import useMaterialUiFormState from "../../../utils/useMaterialUiFormState";
import { REVIEW_STATUS_CHOICES } from "../../../constants";

function AddReviewModalUnconnected({
  card,
  closeModal,
  saveReview,
  CARD_ADD_REVIEW,
}) {
  const [formState, { status, comments }, formErrors, dataFromState] =
    useMaterialUiFormState({
      status: {
        required: true,
      },
      comments: {
        required: true,
      },
    });

  const cardId = card && card.id;

  const latestCall =
    cardId !== null
      ? getLatestMatchingCall({
          callLog: CARD_ADD_REVIEW,
          requestData: { cardId },
        }) || { loading: false }
      : { loading: false };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (latestCall.loading) return;
    const { status, comments } = dataFromState({ state: formState });
    saveReview({ status, comments, cardId });
  };

  const props = {
    card,
    handleSubmit,
    status,
    comments,
    formErrors,
    closeModal,
    statusChoices: REVIEW_STATUS_CHOICES,
    loading: latestCall.loading,
  };
  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  const cardId = state.AddCardReviewModal.cardId;
  const card =
    !!cardId & (state.apiEntities.cards !== undefined)
      ? state.apiEntities.cards[cardId]
      : null;

  return {
    latestApiCallStatus: getLatestMatchingCall({
      callLog: state.CARD_ADD_REVIEW,
      requestData: {},
    }),
    card,
    CARD_ADD_REVIEW: state.CARD_ADD_REVIEW,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    closeModal: () => {
      dispatch(operations.closeCardReviewForm());
    },
    saveReview: ({ cardId, status, comments }) => {
      dispatch(
        apiReduxApps.CARD_ADD_REVIEW.operations.start({
          data: {
            cardId,
            status,
            comments,
          },
        })
      );
    },
  };
};

const AddReviewModal = connect(
  mapStateToProps,
  mapDispatchToProps
)(AddReviewModalUnconnected);

export default AddReviewModal;
