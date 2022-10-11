import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../apiAccess/apiApps";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";
import operations from "./redux/operations.js";
import { REVIEW_STATUS_CHOICES } from "../../../constants";
import { useState } from "react";
import { useEffect } from "react";

function AddReviewModalUnconnected({
  card,
  latestApiCallStatus,
  closeModal,
  saveReview,
  CARD_ADD_REVIEW,
}) {
  const [formValues, setFormValues] = useState({
    status: "",
    comments: "",
  });

  const [isFormValueEmpty, setIsFormValueEmpty] = useState({
    status: false,
    comments: false,
  });

  const [hasFailedApiResponse, setHasFailedApiResponse] = useState(false);

  useEffect(()=>{
    if(latestApiCallStatus){
      if (!latestApiCallStatus.responseOk) setHasFailedApiResponse(true);
    }
  },[latestApiCallStatus])

  const cardId = card && card.id;

  const latestCall =
    cardId !== null
      ? getLatestMatchingCall({
          callLog: CARD_ADD_REVIEW,
          requestData: { cardId },
        }) || { loading: false }
      : { loading: false };

  const handleOnChange = (e) => {
    setIsFormValueEmpty((prev) => ({
      ...prev,
      comments: false,
      status: false,
    }));
    const { name, value } = e.target;
    setFormValues((prevFormValues) => ({ ...prevFormValues, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (formValues.status === "")
      setIsFormValueEmpty((prev) => ({ ...prev, status: true }));
    if (formValues.comments === "")
      setIsFormValueEmpty((prev) => ({ ...prev, comments: true }));

    if (latestCall.loading) return;
    const { comments, status } = formValues;
    saveReview({ status, comments, cardId });
  };

  const props = {
    card,
    hasFailedApiResponse,
    isFormValueEmpty,
    handleSubmit,
    handleOnChange,
    formValues,
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
