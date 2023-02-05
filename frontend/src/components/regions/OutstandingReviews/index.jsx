import { connect } from "react-redux";
import Presentation from "./Presentation";
import React from "react";
import { useParams } from "react-router-dom";

export function OutstandingReviewsModalModalUnconnected({
  outstandingCompetenceReviews,

  // storyData
  forceUser,
}) {
  outstandingCompetenceReviews = outstandingCompetenceReviews || {};
  let urlParams = useParams() || {};
  const userId = forceUser ? forceUser : parseInt(urlParams.userId);

  const cardsNeedingCompetenceReview = Object.values(
    outstandingCompetenceReviews
  ).filter((card) => card.reviewers.includes(userId));

  const props = { cardsNeedingCompetenceReview };
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
