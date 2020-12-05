import {
  //   getAuthToken,
  setAuthToken,
  clearAuthToken,
} from "../utils/authTokenStorage";

import { fetchAndClean } from "./helpers";
import { API_BASE_URL } from "../config";

async function whoAmI() {
  const url = `${API_BASE_URL}/api/who_am_i/`;
  const { response, responseData } = await fetchAndClean({ url });
  if (responseData.detail === "Invalid token.") clearAuthToken();
  return { response, responseData };
}

async function logout() {
  const url = `${API_BASE_URL}/api/logout/`;
  const { response, responseData } = await fetchAndClean({
    url,
    method: "POST",
  });
  clearAuthToken();
  return { response, responseData };
}

async function authenticateWithOneTimeToken(data) {
  const url = `${API_BASE_URL}/social_auth/oauth_one_time_token_auth/`;

  const { response, responseData } = await fetchAndClean({
    url,
    method: "POST",
    data,
  });
  setAuthToken({ value: responseData["token"], keep:true });

  return { response, responseData };
}

async function userGroupsPage({ page }) {
  const url = `${API_BASE_URL}/api/user_groups/?active=true&page=${page}`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function userGroupsEntity({ groupId }) {
  const url = `${API_BASE_URL}/api/user_groups/${groupId}`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function recruitProjectsPage({ userId, page }) {
  const url = `${API_BASE_URL}/api/recruit_projects/?recruit_users=${userId}&page=${page}`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function recruitProjectEntity({ projectId }) {
  const url = `${API_BASE_URL}/api/recruit_projects/${projectId}/`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function topicProgressEntity({ topicProgressId }) {
  const url = `${API_BASE_URL}/api/topic_progress/${topicProgressId}/`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function recruitProjectReviewsPage({ projectId, page }) {
  const url = `${API_BASE_URL}/api/recruit_project_reviews/?recruit_project=${projectId}&page=${page}`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function topicProgressReviewsPage({ topicProgressId, page }) {
  const url = `${API_BASE_URL}/api/topic_reviews/?topic_progress=${topicProgressId}&page=${page}`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function personallyAssignedProjectCardSummariesPage({
  assigneeUserId,
  page,
}) {
  let url = `${API_BASE_URL}/api/project_card_summaries/?page=${page}&assignees=${assigneeUserId}`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function personallyAssignedProjectCardSummaryEntity({ cardId }) {
  let url = `${API_BASE_URL}/api/project_card_summaries/${cardId}`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function personallyAssignedAgileCardsPage({
  assigneeUserId,
  reviewerUserId,
  page,
  status,
}) {
  let url = `${API_BASE_URL}/api/agile_card/?status=${status}&page=${page}`;
  if (assigneeUserId) url += `&assignees=${assigneeUserId}`;
  if (reviewerUserId) url += `&reviewers=${reviewerUserId}`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function agileCardEntity({ cardId }) {
  let url = `${API_BASE_URL}/api/agile_card/${cardId}/`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function cohortsPage({ page }) {
  const url = `${API_BASE_URL}/api/cohorts/?active=true&page=${page}`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function cohortRecruits({ page, cohort }) {
  const url = `${API_BASE_URL}/api/recruit_cohorts/?page=${page}&cohort=${cohort}`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function repositoryEntity({ repositoryId }) {
  const url = `${API_BASE_URL}/api/repository/${repositoryId}`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}
async function repositoryCommitsPage({ repositoryId, page }) {
  const url = `${API_BASE_URL}/api/commit/?page=${page}&repository=${repositoryId}`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}
async function repositoryPullRequestsPage({ repositoryId, page }) {
  const url = `${API_BASE_URL}/api/pull_request/?page=${page}&repository=${repositoryId}`;
  const { response, responseData } = await fetchAndClean({ url });
  return { response, responseData };
}

async function startProject({ cardId }) {
  const url = `${API_BASE_URL}/api/agile_card/${cardId}/start_project/`;
  const { response, responseData } = await fetchAndClean({
    url,
    method: "POST",
  });
  return { response, responseData };
}
async function requestReview({ cardId }) {
  const url = `${API_BASE_URL}/api/agile_card/${cardId}/request_review/`;
  const { response, responseData } = await fetchAndClean({
    url,
    method: "POST",
  });
  return { response, responseData };
}
async function cancelReviewRequest({ cardId }) {
  const url = `${API_BASE_URL}/api/agile_card/${cardId}/cancel_review_request/`;
  const { response, responseData } = await fetchAndClean({
    url,
    method: "POST",
  });
  return { response, responseData };
}
async function addReview({ cardId, status, comments }) {
  const url = `${API_BASE_URL}/api/agile_card/${cardId}/add_review/`;
  const { response, responseData } = await fetchAndClean({
    url,
    method: "POST",
    data: { status, comments },
  });
  return { response, responseData };
}

async function startTopic({ cardId }) {
  const url = `${API_BASE_URL}/api/agile_card/${cardId}/start_topic/`;
  const { response, responseData } = await fetchAndClean({
    url,
    method: "POST",
  });
  return { response, responseData };
}
async function stopTopic({ cardId }) {
  const url = `${API_BASE_URL}/api/agile_card/${cardId}/stop_topic/`;
  const { response, responseData } = await fetchAndClean({
    url,
    method: "POST",
  });
  return { response, responseData };
}
async function finishTopic({ cardId }) {
  const url = `${API_BASE_URL}/api/agile_card/${cardId}/finish_topic/`;
  const { response, responseData } = await fetchAndClean({
    url,
    method: "POST",
  });
  return { response, responseData };
}
async function markWorkshopAttendance({ cardId, timestamp }) {
  const url = `${API_BASE_URL}/api/agile_card/${cardId}/mark_workshop_attendance/`;
  const { response, responseData } = await fetchAndClean({
    url,
    method: "POST",
    data: { timestamp },
  });
  return { response, responseData };
}
async function cancelWorkshopAttendance({ cardId }) {
  const url = `${API_BASE_URL}/api/agile_card/${cardId}/cancel_workshop_attendance/`;
  const { response, responseData } = await fetchAndClean({
    url,
    method: "POST",
  });
  return { response, responseData };
}

async function setProjectLinkSubmission({ cardId, linkSubmission }) {
  const url = `${API_BASE_URL}/api/agile_card/${cardId}/set_project_link/`;
  const { response, responseData } = await fetchAndClean({
    url,
    method: "POST",
    data: {
      linkSubmission,
    },
  });
  return { response, responseData };
}

export default {
  everyone: {
    whoAmI,
    logout,
    authenticateWithOneTimeToken,
    userGroupsPage,
    userGroupsEntity,
  },

  recruits: {
    recruitProjectsPage,
    personallyAssignedAgileCardsPage,

    recruitProjectEntity,
    topicProgressEntity,
    recruitProjectReviewsPage,
    topicProgressReviewsPage,

    repositoryEntity,
    repositoryCommitsPage,
    repositoryPullRequestsPage,

    startProject,
    requestReview,
    cancelReviewRequest,
    addReview,

    startTopic,
    stopTopic,
    finishTopic,

    setProjectLinkSubmission,
  },
  staff: {
    cohortsPage,
    cohortRecruits,
    markWorkshopAttendance,
    cancelWorkshopAttendance,

    personallyAssignedProjectCardSummariesPage,
    personallyAssignedProjectCardSummaryEntity,
    agileCardEntity,
  },
};
