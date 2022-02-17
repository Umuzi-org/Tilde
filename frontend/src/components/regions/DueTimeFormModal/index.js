import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import operations from "./redux/operations";

import { apiReduxApps } from "../../../apiAccess/apiApps"

function DueTimeFormModalUnconnected({
    cardId,
    card,
    handleClose,
    fetchAgileCard,
}) {
    React.useEffect(() => {
        if (cardId && (card === undefined || card === null || card === {})) {
          fetchAgileCard({ cardId });
        }
    }, [
        cardId,
        fetchAgileCard,
        card,
    ]);

    const props = {
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
        users: state.users || {},
        card: state.cards || {},
        authUser: state.App.authUser,
    }
}

const mapDispatchToProps = (dispatch) => {
    return { 
        handleClose: () => { 
            dispatch(operations.closeDueTimeFormModal())
        },

        fetchAgileCard: ({ cardId }) => {
            dispatch(
              apiReduxApps.FETCH_SINGLE_AGILE_CARD.operations.maybeStart({
                data: { cardId },
              })
            );
        },
    }
}

const DueTimeFormModal = connect(
    mapStateToProps,
    mapDispatchToProps
)(DueTimeFormModalUnconnected);
  
export default DueTimeFormModal;