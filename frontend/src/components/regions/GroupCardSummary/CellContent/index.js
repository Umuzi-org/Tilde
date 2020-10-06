import React from "react";
import { connect } from "react-redux";

import Presentation from "./Presentation";
import { cardDetailsModalOperations } from "../../CardDetailsModal/redux";

const SummaryCardUnconnected = ({ card, openCardDetailsModal }) => {
  if (card === undefined) return <div></div>;

  const handleClickOpenCardDetails = () => {
    openCardDetailsModal({ cardId: card.id });
  };

  const props = {
    handleClickOpenCardDetails,
    card,
  };
  return <Presentation {...props} />;
};

const mapStateToProps = (state) => {
  return {};
};
const mapDispatchToProps = (dispatch) => {
  return {
    openCardDetailsModal: ({ cardId }) => {
      dispatch(cardDetailsModalOperations.openCardDetailsModal({ cardId }));
    },
  };
};

const SummaryCard = connect(
  mapStateToProps,
  mapDispatchToProps
)(SummaryCardUnconnected);

export default SummaryCard;
