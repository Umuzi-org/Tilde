import { createReduxApp } from "../../utils/ajaxRedux";
import apiCallers from "../apis";
import { getAuthToken } from "../../utils/authTokenStorage";

const WHO_AM_I = "WHO_AM_I";
const AUTHENTICATE_WITH_ONE_TIME_TOKEN = "AUTHENTICATE_WITH_ONE_TIME_TOKEN";
const LOGOUT = "LOGOUT";

const FETCH_RECRUIT_PROJECTS_PAGE = "FETCH_RECRUIT_PROJECTS_PAGE";
const FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE =
  "FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE";
const FETCH_USER_BURNDOWN_SNAPSHOTS_PAGE =
  "FETCH_USER_BURNDOWN_SNAPSHOTS_PAGE";
const FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE =
  "FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE";
const FETCH_SINGLE_PROJECT_CARD_SUMMARY = "FETCH_SINGLE_PROJECT_CARD_SUMMARY";

const FETCH_COHORTS_PAGE = "FETCH_COHORTS_PAGE";

const FETCH_TOPIC_PROGRESS_REVIEWS_PAGE = "FETCH_TOPIC_PROGRESS_REVIEWS_PAGE";

const FETCH_RECRUIT_PROJECT_REVIEWS_PAGE = "FETCH_RECRUIT_PROJECT_REVIEWS_PAGE";
// const FETCH_VERBOSE_RECRUIT_PROJECT_REVIEWS_PAGE =
//   "FETCH_VERBOSE_RECRUIT_PROJECT_REVIEWS_PAGE";
const FETCH_SINGLE_RECRUIT_PROJECT = "FETCH_SINGLE_RECRUIT_PROJECT";

const FETCH_SINGLE_TEAM = "FETCH_SINGLE_TEAM";
const FETCH_SINGLE_USER = "FETCH_SINGLE_USER";
const FETCH_SINGLE_USER_DETAILED_STATS = "FETCH_SINGLE_USER_DETAILED_STATS";

const FETCH_SINGLE_REPOSITORY = "FETCH_SINGLE_REPOSITORY";
const FETCH_COMMITS_PAGE = "FETCH_COMMITS_PAGE";
const FETCH_PULL_REQUESTS_PAGE = "FETCH_PULL_REQUESTS_PAGE";
const FETCH_TEAMS_PAGE = "FETCH_TEAMS_PAGE";
const FETCH_TEAM_SUMMARY_STATS_PAGE = "FETCH_TEAM_SUMMARY_STATS_PAGE";

const CARD_START_PROJECT = "CARD_START_PROJECT";
const CARD_REQUEST_REVIEW = "CARD_REQUEST_REVIEW";
const CARD_CANCEL_REVIEW_REQUEST = "CARD_CANCEL_REVIEW_REQUEST";
const CARD_ADD_REVIEW = "CARD_ADD_REVIEW";
const CARD_START_TOPIC = "CARD_START_TOPIC";
const CARD_STOP_TOPIC = "CARD_STOP_TOPIC";
const CARD_FINISH_TOPIC = "CARD_FINISH_TOPIC";
const CARD_ADD_WORKSHOP_ATTENDANCE = "CARD_ADD_WORKSHOP_ATTENDANCE";
const CARD_REMOVE_WORKSHOP_ATTENDANCE = "CARD_REMOVE_WORKSHOP_ATTENDANCE";

const CARD_SET_PROJECT_LINK = "CARD_SET_PROJECT_LINK";

const FETCH_SINGLE_AGILE_CARD = "FETCH_SINGLE_AGILE_CARD";

const FETCH_SINGLE_TOPIC_PRGRESS = "FETCH_SINGLE_TOPIC_PRGRESS"; //spelling mistake. fix please

const FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE =
  "FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE";

// if you want to maintain a list of objects returned from some list response, then add that base action type here
export const pagedApiAppTypes = {
  FETCH_RECRUIT_PROJECTS_PAGE: "projects",
  FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE: "cards",
  FETCH_USER_BURNDOWN_SNAPSHOTS_PAGE: "burndownSnapshots",
  FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE: "projectSummaryCards", // TODO rename to summaryCards
  FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE: "projectSummaryCards",
  FETCH_COHORTS_PAGE: "cohorts",
  FETCH_RECRUIT_PROJECT_REVIEWS_PAGE: "projectReviews",
  //   FETCH_VERBOSE_RECRUIT_PROJECT_REVIEWS_PAGE: "FETCH_VERBOSE_RECRUIT_PROJECT_REVIEWS_PAGE"
  FETCH_COMMITS_PAGE: "repoCommits",
  FETCH_PULL_REQUESTS_PAGE: "pullRequests",
  FETCH_TEAMS_PAGE: "teams",
  FETCH_TEAM_SUMMARY_STATS_PAGE: "teamSummaryStats",
  FETCH_TOPIC_PROGRESS_REVIEWS_PAGE: "topicReviews",
};

export const entityApiAppTypes = {
  FETCH_SINGLE_RECRUIT_PROJECT: "projects",
  FETCH_SINGLE_TOPIC_PRGRESS: "topicProgress",
  FETCH_SINGLE_REPOSITORY: "repositories",
  FETCH_SINGLE_TEAM: "teams",
  CARD_START_PROJECT: "cards",
  CARD_REQUEST_REVIEW: "cards",
  CARD_CANCEL_REVIEW_REQUEST: "cards",
  CARD_ADD_REVIEW: "cards",
  CARD_START_TOPIC: "cards",
  CARD_STOP_TOPIC: "cards",
  CARD_FINISH_TOPIC: "cards",
  CARD_ADD_WORKSHOP_ATTENDANCE: "cards",
  CARD_REMOVE_WORKSHOP_ATTENDANCE: "cards",
  FETCH_SINGLE_AGILE_CARD: "cards",
  CARD_SET_PROJECT_LINK: "cards",

  FETCH_SINGLE_PROJECT_CARD_SUMMARY: "projectSummaryCards",
  FETCH_SINGLE_USER: "users",
  FETCH_SINGLE_USER_DETAILED_STATS: "userDetailedStats",
  //   WHO_AM_I: "users",
};

export const apiReduxApps = {
  WHO_AM_I: createReduxApp({
    BASE_TYPE: WHO_AM_I,
    apiCaller: apiCallers.whoAmI,
    reasonsNotToStart: [
      [
        ({ authUser }) => {
          return "isRegistrationComplete" in authUser;
        },
        "Already fetched WhoAmI data",
      ],
      [
        () => {
          return !getAuthToken();
        },
        "cant fetch whoami data: token is missing",
      ],
      [
        () => {
          return true;
        },
        "short circuit",
      ],
    ],
  }),

  AUTHENTICATE_WITH_ONE_TIME_TOKEN: createReduxApp({
    BASE_TYPE: AUTHENTICATE_WITH_ONE_TIME_TOKEN,
    apiCaller: apiCallers.authenticateWithOneTimeToken,
    reasonsNotToStart: [
      [
        ({ authUser }) => {
          return authUser.id || authUser.token;
        },
        "You are already logged in",
      ],
    ],
  }),

  LOGOUT: createReduxApp({
    BASE_TYPE: LOGOUT,
    apiCaller: apiCallers.logout,
    reasonsNotToStart: [],
  }),

  FETCH_RECRUIT_PROJECTS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_RECRUIT_PROJECTS_PAGE,
    apiCaller: apiCallers.recruitProjectsPage,
  }),

  FETCH_TEAMS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_TEAMS_PAGE,
    apiCaller: apiCallers.teamsPage,
  }),

  FETCH_TEAM_SUMMARY_STATS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_TEAM_SUMMARY_STATS_PAGE,
    apiCaller: apiCallers.teamsSummaryStatsPage,
  }),

  FETCH_RECRUIT_PROJECT_REVIEWS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_RECRUIT_PROJECT_REVIEWS_PAGE,
    apiCaller: apiCallers.recruitProjectReviewsPage,
  }),

  FETCH_TOPIC_PROGRESS_REVIEWS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_TOPIC_PROGRESS_REVIEWS_PAGE,
    apiCaller: apiCallers.topicProgressReviewsPage,
  }),

  FETCH_SINGLE_TEAM: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_TEAM,
    apiCaller: apiCallers.teamEntity,
  }),

  FETCH_SINGLE_USER: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_USER,
    apiCaller: apiCallers.userEntity,
  }),

  FETCH_SINGLE_USER_DETAILED_STATS: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_USER_DETAILED_STATS,
    apiCaller: apiCallers.userDetailedStatsEntity,
  }),

  FETCH_SINGLE_RECRUIT_PROJECT: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_RECRUIT_PROJECT,
    apiCaller: apiCallers.recruitProjectEntity,
  }),

  FETCH_SINGLE_TOPIC_PRGRESS: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_TOPIC_PRGRESS,
    apiCaller: apiCallers.topicProgressEntity,
  }),

  FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
    apiCaller: apiCallers.personallyAssignedAgileCardsPage,
  }),

  FETCH_USER_BURNDOWN_SNAPSHOTS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_USER_BURNDOWN_SNAPSHOTS_PAGE,
    apiCaller: apiCallers.userBurndownSnapshotsPage,
  }),

  FETCH_COHORTS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_COHORTS_PAGE,
    apiCaller: apiCallers.cohortsPage,
  }),

  FETCH_SINGLE_REPOSITORY: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_REPOSITORY,
    apiCaller: apiCallers.repositoryEntity,
  }),

  FETCH_COMMITS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_COMMITS_PAGE,
    apiCaller: apiCallers.repositoryCommitsPage,
  }),

  FETCH_PULL_REQUESTS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_PULL_REQUESTS_PAGE,
    apiCaller: apiCallers.repositoryPullRequestsPage,
  }),

  CARD_SET_PROJECT_LINK: createReduxApp({
    BASE_TYPE: CARD_SET_PROJECT_LINK,
    apiCaller: apiCallers.setProjectLinkSubmission,
  }),

  CARD_START_PROJECT: createReduxApp({
    BASE_TYPE: CARD_START_PROJECT,
    apiCaller: apiCallers.startProject,
  }),
  CARD_REQUEST_REVIEW: createReduxApp({
    BASE_TYPE: CARD_REQUEST_REVIEW,
    apiCaller: apiCallers.requestReview,
  }),
  CARD_CANCEL_REVIEW_REQUEST: createReduxApp({
    BASE_TYPE: CARD_CANCEL_REVIEW_REQUEST,
    apiCaller: apiCallers.cancelReviewRequest,
  }),
  CARD_ADD_REVIEW: createReduxApp({
    BASE_TYPE: CARD_ADD_REVIEW,
    apiCaller: apiCallers.addReview,
  }),

  CARD_START_TOPIC: createReduxApp({
    BASE_TYPE: CARD_START_TOPIC,
    apiCaller: apiCallers.startTopic,
  }),

  CARD_STOP_TOPIC: createReduxApp({
    BASE_TYPE: CARD_STOP_TOPIC,
    apiCaller: apiCallers.stopTopic,
  }),

  CARD_FINISH_TOPIC: createReduxApp({
    BASE_TYPE: CARD_FINISH_TOPIC,
    apiCaller: apiCallers.finishTopic,
  }),

  CARD_ADD_WORKSHOP_ATTENDANCE: createReduxApp({
    BASE_TYPE: CARD_ADD_WORKSHOP_ATTENDANCE,
    apiCaller: apiCallers.markWorkshopAttendance,
  }),

  CARD_REMOVE_WORKSHOP_ATTENDANCE: createReduxApp({
    BASE_TYPE: CARD_REMOVE_WORKSHOP_ATTENDANCE,
    apiCaller: apiCallers.cancelWorkshopAttendance,
  }),

  FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE: createReduxApp({
    BASE_TYPE: FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE,
    apiCaller: apiCallers.personallyAssignedCardSummariesPage,
  }),

  FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE: createReduxApp({
    BASE_TYPE: FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE,
    apiCaller: apiCallers.userActionsCardsCompletedPage,
  }),

  FETCH_SINGLE_PROJECT_CARD_SUMMARY: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_PROJECT_CARD_SUMMARY,
    apiCaller: apiCallers.personallyAssignedCardSummaryEntity,
  }),

  FETCH_SINGLE_AGILE_CARD: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_AGILE_CARD,
    apiCaller: apiCallers.agileCardEntity,
  }),
};

let allReducers = {};
Object.keys(apiReduxApps).forEach((key) => {
  allReducers[key] = apiReduxApps[key].reducer;
});

export const apiReduxReducers = { ...allReducers };

export const apiReduxWatchers = Object.keys(apiReduxApps)
  .map((key) => {
    return apiReduxApps[key].sagaWatchers;
  })
  .flat();
