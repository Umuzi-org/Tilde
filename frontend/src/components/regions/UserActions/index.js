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
        // { page: 1, recruitUsers: [userId] },
      ],
    });
  }, [fetchProjectReviewsPages, userId]);

  const handleClickOpenProjectDetails = ({ cardId }) => {
    // console.log(review.agileCard);
    openCardDetailsModal({ cardId });
  };

  const days = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];
  const reviewsDone = Object.values(projectReviews)
    .filter((review) => review.reviewerUser === userId)
    .map((review) => {
      const timestamp = new Date(review.timestamp);
      const dateStr =
        days[timestamp.getDay()] + " " + timestamp.toLocaleDateString();
      return {
        ...review,
        timestamp,
        actionType: "Review Done",
        dateStr,
      };
    });

  let actionLog = reviewsDone;
  actionLog.sort((action1, action2) => action2.timestamp - action1.timestamp);

  let orderedDates = [];

  let actionLogByDate = {};
  actionLog.forEach((o) => {
    const date = o.dateStr;
    if (orderedDates.indexOf(date) === -1) orderedDates.push(date);
    actionLogByDate[date] = actionLogByDate[date] || [];
    actionLogByDate[date].push(o);
  });

  const props = {
    orderedDates,
    actionLogByDate,
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
