import { connect } from "react-redux";
import Presentation from "./Presentation";
import React from "react";

export function OutstandingReviewsModalModalUnconnected({
  cardsNeedingCompetenceReview,
  open,
  handleClose,
}) {
  const props = { cardsNeedingCompetenceReview, open, handleClose };
  return <Presentation {...props} />;
}

const mapDispatchToProps = (dispatch) => {
  return {};
};

const mapStateToProps = (state) => {
  return {};
};

const OutstandingReviewsModal = connect(
  mapStateToProps,
  mapDispatchToProps
)(OutstandingReviewsModalModalUnconnected);

export default OutstandingReviewsModal;
