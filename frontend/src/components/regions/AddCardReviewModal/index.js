import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../apiAccess/redux/apiApps";
import { getLatestMatchingCall } from "../../../utils/ajaxRedux";
import operations from "./redux/operations.js";
import useMaterialUiFormState from "../../../utils/useMaterialUiFormState";

import { REVIEW_STATUS_CHOICES } from "../../../constants";

const AddReviewModalUnconnected = ({ card, closeModal, saveReview }) => {
  const [
    formState,
    { status, comments },
    formErrors,
    dataFromState,
  ] = useMaterialUiFormState({
    status: {
      required: true,
    },
    comments: {
      required: true,
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    const { status, comments } = dataFromState({ state: formState });
    saveReview({ status, comments, cardId: card.id });
  };

  const props = {
    card,
    handleSubmit,
    status,
    comments,
    formErrors,
    closeModal,
    statusChoices: REVIEW_STATUS_CHOICES,
  };
  return <Presentation {...props} />;
};

const mapStateToProps = (state) => {
  const cardId = state.AddCardReviewModal.cardId;
  const card =
    !!cardId & (state.Entities.cards !== undefined)
      ? state.Entities.cards[cardId]
      : null;

  return {
    latestApiCallStatus: getLatestMatchingCall({
      callLog: state.CARD_ADD_REVIEW,
      requestData: {},
    }),
    card,
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
