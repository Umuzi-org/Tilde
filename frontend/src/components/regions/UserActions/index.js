import React from "react";
import Presentation from "./Presentation";
// import { useParams } from "react-router-dom";
// https://api.github.com/users/sheenarbw/events
import { useParams } from "react-router-dom";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../apiAccess/redux/apiApps";

import { cardDetailsModalOperations } from "../CardDetailsModal/redux";

function UserActionsUnconnected({
  authedUserId,
  projectReviews,
  fetchProjectReviewsPages,
  openCardDetailsModal,
}) {
  let urlParams = useParams() || {};
  const userId = parseInt(urlParams.userId || authedUserId || 0);

  React.useEffect(() => {
    fetchProjectReviewsPages({
      dataSequence: [
        { page: 1, reviewerUser: userId },
        { page: 1, recruitUsers: [userId] },
      ],
    });
  }, [fetchProjectReviewsPages, userId]);

  const handleClickOpenProjectDetails = ({ review }) => {
    // console.log(review.agileCard);
    openCardDetailsModal({ cardId: review.agileCard });
  };

  let allReviews = Object.values(projectReviews);

  allReviews = allReviews.map((review) => ({
    ...review,
    timestamp: new Date(review.timestamp),
  }));

  allReviews.sort((review1, review2) => review1.timestamp - review2.timestamp);
  const reviewsDone = allReviews.filter(
    (review) => review.reviewerUser === userId
  );

  const reviewsRecieved = allReviews.filter(
    (review) => review.reviewedUserIds.indexOf(authedUserId) !== -1
  );

  const props = {
    reviewsDone,
    reviewsRecieved,
    handleClickOpenProjectDetails,
  };
  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    users: state.Entities.users || {},
    projectReviews: state.Entities.projectReviews || {},
    authedUserId: state.App.authUser.userId,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchProjectReviewsPages: ({ dataSequence }) => {
      dispatch(
        apiReduxApps.FETCH_RECRUIT_PROJECT_REVIEWS_PAGE.operations.startCallSequence(
          { dataSequence }
        )
      );
    },

    fetchUser: ({ userId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_USER.operations.maybeStart({
          data: { userId },
        })
      );
    },

    openCardDetailsModal: ({ cardId }) => {
      dispatch(cardDetailsModalOperations.openCardDetailsModal({ cardId }));
    },
  };
};

const UserActions = connect(
  mapStateToProps,
  mapDispatchToProps
)(UserActionsUnconnected);

export default UserActions;
