// import { createReduxApp } from "../../utils/ajaxRedux";
import apiCallers from "./apis";
import { getAuthToken } from "../utils/authTokenStorage";
import { createReduxApp } from "@prelude/redux-api-toolbox/src/appCreator";

const WHO_AM_I = "WHO_AM_I";
const AUTHENTICATE_WITH_ONE_TIME_TOKEN = "AUTHENTICATE_WITH_ONE_TIME_TOKEN";
const LOGOUT = "LOGOUT";

const FETCH_RECRUIT_PROJECTS_PAGE = "FETCH_RECRUIT_PROJECTS_PAGE";
const FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE =
  "FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE";
const FETCH_USER_BURNDOWN_SNAPSHOTS_PAGE = "FETCH_USER_BURNDOWN_SNAPSHOTS_PAGE";
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
const FETCH_AGILE_CARDS_THAT_REQUIRE_CARD =
  "FETCH_AGILE_CARDS_THAT_REQUIRE_CARD";

const FETCH_SINGLE_TOPIC_PROGRESS = "FETCH_SINGLE_TOPIC_PROGRESS"; //spelling mistake. fix please

const FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE =
  "FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE";

const FETCH_ACTIVITY_LOG_DAY_COUNTS_PAGE = "FETCH_ACTIVITY_LOG_DAY_COUNTS_PAGE";

const FETCH_ACTIVITY_LOG_ENTRIES = "FETCH_ACTIVITY_LOG_ENTRIES";

const FETCH_COMPETENCE_REVIEW_QUEUE_PAGE = "FETCH_COMPETENCE_REVIEW_QUEUE_PAGE";
const FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE =
  "FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE";

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

  FETCH_ACTIVITY_LOG_DAY_COUNTS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_ACTIVITY_LOG_DAY_COUNTS_PAGE,
    apiCaller: apiCallers.activityLogDayCountsPage,
    responseIsList: true,
    responseEntityType: "activityLogDayCounts",
  }),

  FETCH_RECRUIT_PROJECTS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_RECRUIT_PROJECTS_PAGE,
    apiCaller: apiCallers.recruitProjectsPage,
    responseIsList: true,
    responseEntityType: "projects",
  }),

  FETCH_TEAMS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_TEAMS_PAGE,
    apiCaller: apiCallers.teamsPage,
    responseIsList: true,
    responseEntityType: "teams",
  }),

  FETCH_TEAM_SUMMARY_STATS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_TEAM_SUMMARY_STATS_PAGE,
    apiCaller: apiCallers.teamsSummaryStatsPage,

    responseIsList: true,
    responseEntityType: "teamSummaryStats",
  }),

  FETCH_RECRUIT_PROJECT_REVIEWS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_RECRUIT_PROJECT_REVIEWS_PAGE,
    apiCaller: apiCallers.recruitProjectReviewsPage,
    responseIsList: true,
    responseEntityType: "projectReviews",
  }),

  FETCH_TOPIC_PROGRESS_REVIEWS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_TOPIC_PROGRESS_REVIEWS_PAGE,
    apiCaller: apiCallers.topicProgressReviewsPage,
    responseIsList: true,
    responseEntityType: "topicReviews",
  }),

  FETCH_SINGLE_TEAM: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_TEAM,
    apiCaller: apiCallers.teamEntity,
    responseIsList: false,
    responseEntityType: "teams",
  }),

  FETCH_SINGLE_USER: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_USER,
    apiCaller: apiCallers.userEntity,
    responseIsList: false,
    responseEntityType: "users",
  }),

  FETCH_SINGLE_USER_DETAILED_STATS: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_USER_DETAILED_STATS,
    apiCaller: apiCallers.userDetailedStatsEntity,
    responseIsList: false,
    responseEntityType: "userDetailedStats",
  }),

  FETCH_SINGLE_RECRUIT_PROJECT: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_RECRUIT_PROJECT,
    apiCaller: apiCallers.recruitProjectEntity,
    responseIsList: false,
    responseEntityType: "projects",
  }),

  FETCH_SINGLE_TOPIC_PROGRESS: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_TOPIC_PROGRESS,
    apiCaller: apiCallers.topicProgressEntity,
    responseIsList: false,
    responseEntityType: "topicProgress",
  }),

  FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_PERSONALLY_ASSIGNED_AGILE_CARDS_PAGE,
    apiCaller: apiCallers.personallyAssignedAgileCardsPage,
    responseIsList: true,
    responseEntityType: "cards",
  }),

  FETCH_AGILE_CARDS_THAT_REQUIRE_CARD: createReduxApp({
    BASE_TYPE: FETCH_AGILE_CARDS_THAT_REQUIRE_CARD,
    apiCaller: apiCallers.agileCardsThatRequireCard,
    responseIsList: true,
    responseEntityType: "cards",
  }),

  FETCH_USER_BURNDOWN_SNAPSHOTS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_USER_BURNDOWN_SNAPSHOTS_PAGE,
    apiCaller: apiCallers.userBurndownSnapshotsPage,
    responseIsList: true,
    responseEntityType: "burndownSnapshots",
  }),

  FETCH_COHORTS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_COHORTS_PAGE,
    apiCaller: apiCallers.cohortsPage,
    responseEntityType: "cohorts", // TODO: rename to teams. Or remove this if we dont use it
    responseIsList: true,
  }),

  FETCH_SINGLE_REPOSITORY: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_REPOSITORY,
    apiCaller: apiCallers.repositoryEntity,
    responseIsList: false,
    responseEntityType: "repositories",
  }),

  FETCH_COMMITS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_COMMITS_PAGE,
    apiCaller: apiCallers.repositoryCommitsPage,
    responseEntityType: "repoCommits",
    responseIsList: true,
  }),

  FETCH_PULL_REQUESTS_PAGE: createReduxApp({
    BASE_TYPE: FETCH_PULL_REQUESTS_PAGE,
    apiCaller: apiCallers.repositoryPullRequestsPage,
    responseEntityType: "pullRequests",
    responseIsList: true,
  }),

  CARD_SET_PROJECT_LINK: createReduxApp({
    BASE_TYPE: CARD_SET_PROJECT_LINK,
    apiCaller: apiCallers.setProjectLinkSubmission,
    responseEntityType: "cards",
    responseIsList: false,
  }),

  CARD_START_PROJECT: createReduxApp({
    BASE_TYPE: CARD_START_PROJECT,
    apiCaller: apiCallers.startProject,
    responseEntityType: "cards",
    responseIsList: false,
  }),
  CARD_REQUEST_REVIEW: createReduxApp({
    BASE_TYPE: CARD_REQUEST_REVIEW,
    apiCaller: apiCallers.requestReview,
    responseEntityType: "cards",
    responseIsList: false,
  }),
  CARD_CANCEL_REVIEW_REQUEST: createReduxApp({
    BASE_TYPE: CARD_CANCEL_REVIEW_REQUEST,
    apiCaller: apiCallers.cancelReviewRequest,
    responseEntityType: "cards",
    responseIsList: false,
  }),
  CARD_ADD_REVIEW: createReduxApp({
    BASE_TYPE: CARD_ADD_REVIEW,
    apiCaller: apiCallers.addReview,
    responseEntityType: "cards",
    responseIsList: false,
  }),

  CARD_START_TOPIC: createReduxApp({
    BASE_TYPE: CARD_START_TOPIC,
    apiCaller: apiCallers.startTopic,
    responseEntityType: "cards",
    responseIsList: false,
  }),

  CARD_STOP_TOPIC: createReduxApp({
    BASE_TYPE: CARD_STOP_TOPIC,
    apiCaller: apiCallers.stopTopic,
    responseEntityType: "cards",
    responseIsList: false,
  }),

  CARD_FINISH_TOPIC: createReduxApp({
    BASE_TYPE: CARD_FINISH_TOPIC,
    apiCaller: apiCallers.finishTopic,
    responseEntityType: "cards",
    responseIsList: false,
  }),

  CARD_ADD_WORKSHOP_ATTENDANCE: createReduxApp({
    BASE_TYPE: CARD_ADD_WORKSHOP_ATTENDANCE,
    apiCaller: apiCallers.markWorkshopAttendance,
    responseEntityType: "cards",
    responseIsList: false,
  }),

  CARD_REMOVE_WORKSHOP_ATTENDANCE: createReduxApp({
    BASE_TYPE: CARD_REMOVE_WORKSHOP_ATTENDANCE,
    apiCaller: apiCallers.cancelWorkshopAttendance,
    responseEntityType: "cards",
    responseIsList: false,
  }),

  FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE: createReduxApp({
    BASE_TYPE: FETCH_PERSONALLY_ASSIGNED_PROJECT_CARD_SUMMARY_PAGE,
    apiCaller: apiCallers.personallyAssignedCardSummariesPage,
    responseIsList: true,
    responseEntityType: "projectSummaryCards", // TODO: rename to summaryCards
  }),

  FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE: createReduxApp({
    BASE_TYPE: FETCH_USER_ACTIONS_CARDS_COMPLETED_PAGE,
    apiCaller: apiCallers.userActionsCardsCompletedPage,
    responseIsList: true,
    responseEntityType: "projectSummaryCards",
  }),

  FETCH_SINGLE_PROJECT_CARD_SUMMARY: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_PROJECT_CARD_SUMMARY,
    apiCaller: apiCallers.personallyAssignedCardSummaryEntity,
    responseEntityType: "projectSummaryCards",
    responseIsList: false,
  }),

  FETCH_SINGLE_AGILE_CARD: createReduxApp({
    BASE_TYPE: FETCH_SINGLE_AGILE_CARD,
    apiCaller: apiCallers.agileCardEntity,
    responseEntityType: "cards",
    responseIsList: false,
  }),

  FETCH_ACTIVITY_LOG_ENTRIES: createReduxApp({
    BASE_TYPE: FETCH_ACTIVITY_LOG_ENTRIES,
    apiCaller: apiCallers.activityLogEntries,
    responseIsList: true,
    responseEntityType: "activityLogEntries",
  }),

  FETCH_COMPETENCE_REVIEW_QUEUE_PAGE: createReduxApp({
    BASE_TYPE: FETCH_COMPETENCE_REVIEW_QUEUE_PAGE,
    apiCaller: apiCallers.competenceReviewQueue,
    responseIsList: true,
    responseEntityType: "competenceReviewQueueProject",
  }),

  FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE: createReduxApp({
    BASE_TYPE: FETCH_PULL_REQUEST_REVIEW_QUEUE_PAGE,
    apiCaller: apiCallers.pullRequestReviewQueue,
    responseIsList: true,
    responseEntityType: "pullRequestReviewQueueProject",
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
