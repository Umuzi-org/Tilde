import React from "react";
import { connect } from "react-redux";

import Presentation from "./Presentation";

function SummaryCardUnconnected ({ card }) {
  if (card === undefined) return <div></div>;

  const props = {
    card,
  };
  return <Presentation {...props} />;
};

const mapStateToProps = (state) => {
  return {};
};
const mapDispatchToProps = (dispatch) => {
  return {};
};

const SummaryCard = connect(
  mapStateToProps,
  mapDispatchToProps
)(SummaryCardUnconnected);

export default SummaryCard;
