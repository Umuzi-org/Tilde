import React from "react";
import { connect } from "react-redux";

import Presentation from "./Presentation";
import { cardDetailsModalOperations } from "../../../CardDetailsModal/redux";

const SummaryCardUnconnected = ({ card, openCardDetailsModal }) => {
  const handleClickOpenDetails = () => {
    openCardDetailsModal({ cardId: card.id });
  };

  const props = {
    handleClickOpenDetails,
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
