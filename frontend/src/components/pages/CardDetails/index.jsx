import React, { useEffect } from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";

import { apiReduxApps } from "../../../apiAccess/apiApps";
import { addCardReviewOperations } from "../../regions/AddCardReviewModal/redux";
import useMaterialUiFormState from "../../../utils/useMaterialUiFormState";

import { REVIEW_FEEDBACK, IN_PROGRESS } from "../../../constants";

function CardDetailsUnconnected({
  cards,
  projects,
  topicProgressArray,
  projectReviews,
  topicReviews,
  authUser,
  // viewedUser,

  openReviewFormModal,
  updateProjectLink,
  fetchProject,
  fetchProjectReviews,
  fetchTopicProgress,
  fetchTopicReviews,
  fetchAgileCard,
}) {
  let urlParams = useParams() || {};
  const { cardId } = urlParams;
  const card = cards && cards[cardId];

  const projectId =
    card && card.contentTypeNice === "project" && card.recruitProject;
  const project =
    !!projectId & (projects !== undefined) ? projects[projectId] : null;

  const topicProgressId =
    card && card.contentTypeNice === "topic" && card.topicProgress;
  const topicProgress =
    !!topicProgressId & (topicProgressArray !== undefined)
      ? topicProgressArray[topicProgressId]
      : null;

  useEffect(() => {
    if (projectId) {
      fetchProject({ projectId });
      fetchProjectReviews({ projectId });
    }

    if (topicProgressId) {
      fetchTopicProgress({ topicProgressId });
      fetchTopicReviews({ topicProgressId });
    }
    if (cardId && (card === undefined || card === null || card === {})) {
      fetchAgileCard({ cardId });
    }
  }, [
    projectId,
    fetchProject,
    fetchProjectReviews,
    topicProgressId,
    fetchTopicProgress,
    fetchTopicReviews,
    cardId,
    fetchAgileCard,
    card,
  ]);

  const [
    formState,
    { linkSubmission },
    formErrors,
    dataFromState,
  ] = useMaterialUiFormState({
    linkSubmission: {
      required: true,
    },
  });

  const handleClickUpdateProjectLink = (e) => {
    e.preventDefault();
    const { linkSubmission } = dataFromState({ state: formState });
    updateProjectLink({ linkSubmission, cardId: project.agileCard });
  };

  const handleClickAddReview = () => {
    openReviewFormModal({ cardId: project.agileCard });
  };

  const isAssignee =
    ((project || {}).recruitUsers || []).indexOf(authUser.userId) !== -1;

  // const isReviewer =
  //   ((project || {}).reviewerUsers || []).indexOf(authUser.userId) !== -1;

  const projectCardStatus = project && project.agileCardStatus;

  // const cardWithStatusOnly = { status: projectCardStatus };

  // const permissions = getTeamPermissions({ authUser, viewedUser });

  // const showAddReviewButton = getShowAddReviewButton({   // TODO: fix
  //   card: cardWithStatusOnly,
  //   permissions,
  //   isReviewer,
  // });
  const showUpdateProjectLinkForm =
    isAssignee &&
    [REVIEW_FEEDBACK, IN_PROGRESS].indexOf(projectCardStatus) !== -1;

  const currentProjectReviews =
    project && projectReviews
      ? project.projectReviews
          .map((reviewId) => projectReviews[reviewId])
          .filter((review) => review !== undefined)
      : [];

  const currentTopicReviews =
    topicProgress && topicReviews
      ? topicProgress.topicReviews
          .map((reviewId) => topicReviews[reviewId])
          .filter((review) => review !== undefined)
      : [];

  const props = {
    project,
    projectId,
    cardId,
    card,
    topicProgressId,
    topicProgress,
    topicReviews: currentTopicReviews,
    projectReviews: currentProjectReviews,

    handleClickAddReview,
    // showAddReviewButton,
    showUpdateProjectLinkForm,
    handleClickUpdateProjectLink,

    linkSubmission,
    formErrors,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    cards: state.apiEntities.cards,
    projects: state.apiEntities.projects,
    topicProgressArray: state.apiEntities.topicProgress,
    projectReviews: state.apiEntities.projectReviews,
    topicReviews: state.apiEntities.topicReviews,

    authUser: state.App.authUser,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchAgileCard: ({ cardId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_AGILE_CARD.operations.maybeStart({
          data: { cardId },
        })
      );
    },

    fetchProject: ({ projectId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_RECRUIT_PROJECT.operations.maybeStart({
          data: {
            projectId,
          },
        })
      );
    },

    fetchProjectReviews: ({ projectId }) => {
      dispatch(
        apiReduxApps.FETCH_RECRUIT_PROJECT_REVIEWS_PAGE.operations.maybeStart({
          data: {
            projectId,
            page: 1,
          },
        })
      );
    },

    fetchTopicProgress: ({ topicProgressId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_TOPIC_PROGRESS.operations.maybeStart({
          data: {
            topicProgressId,
          },
        })
      );
    },
    fetchTopicReviews: ({ topicProgressId }) => {
      dispatch(
        apiReduxApps.FETCH_TOPIC_PROGRESS_REVIEWS_PAGE.operations.maybeStart({
          data: {
            topicProgressId,
            page: 1,
          },
        })
      );
    },

    openReviewFormModal: ({ cardId }) => {
      dispatch(addCardReviewOperations.openCardReviewForm({ cardId }));
    },

    updateProjectLink: ({ cardId, linkSubmission }) => {
      dispatch(
        apiReduxApps.CARD_SET_PROJECT_LINK.operations.maybeStart({
          data: { cardId, linkSubmission },
        })
      );
    },
  };
};

const CardDetails = connect(
  mapStateToProps,
  mapDispatchToProps
)(CardDetailsUnconnected);

export default CardDetails;
