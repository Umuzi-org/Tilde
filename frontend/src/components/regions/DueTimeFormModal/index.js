import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import operations from "./redux/operations";

export const DueTimeFormModalUnconnected = ({ cardId, card, closeModal }) => {
    return (
        <Presentation card={card} closeModal={closeModal} />
    )
}

const mapStateToProps = (state) => {
    const cardId = state.DueTimeFormModal.cardId;
    const card = 
        !!cardId && (state.Entities.cards !== undefined) 
        ? state.Entities.cards[cardId] 
        : null;
    return {
        cardId,
        card,
    }
}

const mapDispatchToProps = (dispatch) => {
    return { 
        closeModal: () => { 
            dispatch(operations.closeDueTimeFormModal())
        }
    }
}

const DueTimeFormModal = connect(
    mapStateToProps,
    mapDispatchToProps
)(DueTimeFormModalUnconnected);
  
export default DueTimeFormModal;