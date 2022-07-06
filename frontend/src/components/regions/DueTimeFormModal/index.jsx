import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import operations from "./redux/operations";

import { apiReduxApps } from "../../../apiAccess/apiApps";

function DueTimeFormModalUnconnected({
  users,
  cardId,
  card,
  handleClose,
  fetchAgileCard,
  setDueTime,
}) {
  React.useEffect(() => {
    if (cardId && (card === undefined || card === null || card === {})) {
      fetchAgileCard({ cardId });
    }
  }, [cardId, fetchAgileCard, card]);

  const viewedUser =
    card.assignees === undefined ? null : users[card.assignees[0]];

  const props = {
    viewedUser,
    cardId,
    card,
    handleClose,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    ...state,
    cardId: state.DueTimeFormModal.cardId || null,
    users: state.apiEntities.user || {},
    card: state.apiEntities.cards || {},
    authUser: state.apiEntities.authUser,
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
    setDueTime: ({ cardId, dueTime }) => {
      dispatch(
        apiReduxApps.CARD_SET_DUE_TIME.operations.start({
          data: {
            cardId,
            dueTime,
          },
        })
      );
    }
  };
};

const DueTimeFormModal = connect(
  mapStateToProps,
  mapDispatchToProps
)(DueTimeFormModalUnconnected);

export default DueTimeFormModal;
