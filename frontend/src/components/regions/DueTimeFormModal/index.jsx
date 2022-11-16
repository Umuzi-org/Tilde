import React, { useEffect, useState } from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import operations from "./redux/operations";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";
import { apiReduxApps } from "../../../apiAccess/apiApps";

function DueTimeFormModalUnconnected({
  users,
  cardId,
  cards,
  handleClose,
  fetchAgileCard,
  setCardDueTime,
  CARD_SET_DUE_TIME,
}) {
  const [dueTime, setDueTime] = useState(cards.dueTime || "");
  useEffect(() => {
    if (cardId && (cards === undefined || cards === null || cards === {})) {
      fetchAgileCard({ cardId });
    }
  }, [cardId, fetchAgileCard, cards]);

  const viewedUser =
    cards.assignees === undefined ? null : users[cards.assignees[0]];

  const latestCall =
    cardId !== null
      ? getLatestMatchingCall({
          callLog: CARD_SET_DUE_TIME,
          requestData: { cardId },
        }) || { loading: false }
      : { loading: false };

  const handleSubmit = (dueTime) => {
    if (latestCall.loading) return;
    setCardDueTime({ cardId, dueTime });
    handleClose();
  };

  const props = {
    viewedUser,
    cardId,
    cards,
    dueTime,
    setDueTime,
    handleClose,
    handleSubmit,
    loading: latestCall.loading,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    ...state,
    latestApiCallStatus: getLatestMatchingCall({
      callLog: state.CARD_SET_DUE_TIME,
      requestData: {},
    }),
    cardId: state.DueTimeFormModal.cardId || null,
    users: state.apiEntities.user || {},
    cards: state.apiEntities.cards || {},
    authUser: state.apiEntities.authUser,
    CARD_SET_DUE_TIME: state.CARD_SET_DUE_TIME,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    handleClose: () => {
      dispatch(operations.closeDueTimeFormModal());
    },
    fetchAgileCard: ({ cardId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_AGILE_CARD.operations.maybeStart({
          data: { cardId },
        })
      );
    },
    setCardDueTime: ({ cardId, dueTime }) => {
      dispatch(
        apiReduxApps.CARD_SET_DUE_TIME.operations.start({
          data: {
            cardId,
            dueTime,
          },
        })
      );
    },
  };
};

const DueTimeFormModal = connect(
  mapStateToProps,
  mapDispatchToProps
)(DueTimeFormModalUnconnected);

export default DueTimeFormModal;
