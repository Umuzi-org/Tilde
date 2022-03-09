import {
    READY,
    REVIEW_FEEDBACK,
    COMPLETE,
    BLOCKED,
    IN_PROGRESS,
    IN_REVIEW,
    TEAM_PERMISSIONS,
    MANAGE_CARDS,
    REVIEW_CARDS,
    TRUSTED_REVIEWER,
  } from "../constants";
  
  export function getTeamPermissions({ authUser, viewedUser }) {
    let result = {};
  
    for (let permission of TEAM_PERMISSIONS) result[permission] = false;
  
    if (authUser.isSuperuser) {
      for (let permission of TEAM_PERMISSIONS) result[permission] = true;
    } else {
      // we look at what teams this user belongs to. If authUser has a permission on one of those teams then they have the permission for the user
      for (let authedTeamId in authUser.permissions.teams) {
        if (viewedUser.teamMemberships[authedTeamId]) {
          let heldPermissions =
            authUser.permissions.teams[authedTeamId].permissions;
          for (let permission of heldPermissions) {
            result[permission] = true;
          }
        }
      }
    }
    return result;
  }
  
  function getShowAddReviewButton({ card, permissions, isReviewer }) {
    const REVIEW_STATUSES = [IN_REVIEW, COMPLETE, REVIEW_FEEDBACK];
    if (isReviewer && REVIEW_STATUSES.indexOf(card.status) !== -1) return true;
    if (
      (permissions[REVIEW_CARDS] || permissions[TRUSTED_REVIEWER]) &&
      REVIEW_STATUSES.indexOf(card.status) !== -1
    )
      return true;
  
    return false;
  }
  
  function getReviewRequestButtons({ card, permissions, isAssignee }) {
    let showButtonRequestReview = false;
    let showButtonCancelReviewRequest = false;
    if (isAssignee || permissions[MANAGE_CARDS]) {
      if (card.status === IN_PROGRESS) showButtonRequestReview = true;
      if (card.status === REVIEW_FEEDBACK) showButtonRequestReview = true;
      if (card.status === IN_REVIEW) showButtonCancelReviewRequest = true;
    }
  
    return {
      showButtonRequestReview,
      showButtonCancelReviewRequest,
    };
  }
  
  export function showButtons({ card, authUser, viewedUser }) {
    let showButtonStartProject = false;
    let showButtonNoteWorkshopAttendance = false;
    let showButtonCancelWorkshopAttendance = false;
  
    let showButtonStartTopic = false;
    let showButtonStopTopic = false;
    let showButtonEndTopic = false;
  
    let showButtonAddReview = false;
    let showButtonRequestReview = false;
    let showButtonCancelReviewRequest = false;
  
    const isAssignee = card.assignees.indexOf(authUser.userId) !== -1;
    const isReviewer = card.reviewers.indexOf(authUser.userId) !== -1;
    const permissions = getTeamPermissions({ authUser, viewedUser });
  
    let reviewRequestButtons;
    if (card.contentTypeNice === "project") {
      // PROJECT CARDS
  
      if (isAssignee && card.canStart) showButtonStartProject = true;
      if (permissions[MANAGE_CARDS] & card.canForceStart)
        showButtonStartProject = true;
  
      showButtonAddReview = getShowAddReviewButton({
        card,
        permissions,
        isReviewer,
      });
      reviewRequestButtons = getReviewRequestButtons({
        card,
        permissions,
        isAssignee,
      });
      showButtonRequestReview = reviewRequestButtons.showButtonRequestReview;
      showButtonCancelReviewRequest =
        reviewRequestButtons.showButtonCancelReviewRequest;
    } else if (card.contentTypeNice === "workshop") {
      // WORKSHOP CARDS
  
      if (permissions[MANAGE_CARDS] & (card.status === READY))
        showButtonNoteWorkshopAttendance = true;
      if (permissions[MANAGE_CARDS] & (card.status === BLOCKED))
        showButtonNoteWorkshopAttendance = true;
      if (permissions[MANAGE_CARDS] & (card.status === COMPLETE))
        showButtonCancelWorkshopAttendance = true;
    } else if (card.contentTypeNice === "topic") {
      // TOPIC CARDS
  
      if (isAssignee && card.canStart) showButtonStartTopic = true;
      if (permissions[MANAGE_CARDS] & card.canForceStart)
        showButtonStartTopic = true;
      if (
        (permissions[MANAGE_CARDS] || isAssignee) &&
        card.status === IN_PROGRESS
      ) {
        showButtonStopTopic = true;
        showButtonEndTopic = true;
      }
      if (permissions[MANAGE_CARDS] && card.status === IN_PROGRESS) {
        showButtonStopTopic = true;
      }
      if (card.topicNeedsReview) {
        showButtonEndTopic = false;
  
        showButtonAddReview = getShowAddReviewButton({
          card,
          permissions,
          isReviewer,
        });
        reviewRequestButtons = getReviewRequestButtons({
          card,
          permissions,
          isAssignee,
        });
        showButtonRequestReview = reviewRequestButtons.showButtonRequestReview;
        showButtonCancelReviewRequest =
          reviewRequestButtons.showButtonCancelReviewRequest;
      }
    } else {
      throw new Error(`Error: unknown content type: ${card.contentTypeNice}`);
    }
  
    return {
      showButtonStartProject,
      showButtonAddReview,
  
      showButtonRequestReview,
      showButtonCancelReviewRequest,
      showButtonStartTopic,
      showButtonStopTopic,
      showButtonEndTopic,
      showButtonNoteWorkshopAttendance,
      showButtonCancelWorkshopAttendance,
      // showButtonPauseProject // TODO. unstart project
    };
  }