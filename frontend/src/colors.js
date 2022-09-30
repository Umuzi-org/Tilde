import {
  READY,
  BLOCKED,
  COMPLETE,
  IN_REVIEW,
  IN_PROGRESS,
  REVIEW_FEEDBACK,
  CARD_MOVED_TO_COMPLETE,
  CARD_MOVED_TO_REVIEW_FEEDBACK,
  CARD_REVIEW_REQUESTED,
  CARD_REVIEW_REQUEST_CANCELLED,
  CARD_STARTED,
  PR_REVIEWED,
  COMPETENCE_REVIEW_DONE,
  INCORRECT,
  CORRECT,
  CONTRADICTED,
} from "./constants";
import { colors } from "@material-ui/core";

export const cardColors = {
  [COMPLETE]: colors.yellow[600],
  [IN_REVIEW]: colors.orange[600],
  [REVIEW_FEEDBACK]: colors.red[600],
  [IN_PROGRESS]: colors.green[600],
  [READY]: colors.blue[600],
  [BLOCKED]: colors.grey[600],
};

export const eventTypeColors = {
  [CARD_MOVED_TO_COMPLETE]: colors.yellow[600],
  [CARD_MOVED_TO_REVIEW_FEEDBACK]: colors.red[600],
  [CARD_REVIEW_REQUESTED]: colors.orange[600],
  [CARD_REVIEW_REQUEST_CANCELLED]: colors.grey[600],
  [CARD_STARTED]: colors.green[600],
  [PR_REVIEWED]: colors.purple[600],
  [COMPETENCE_REVIEW_DONE]: colors.blue[600],
};

export const reviewValidatedColors = {
  [INCORRECT]: colors.red[600],
  [CORRECT]: colors.green[600],
  [CONTRADICTED]: colors.orange[600],
};

export const trustedColor = colors.yellow[600];

export const completeReviewCycleColors = {
  [true]: colors.blue[600],
  [false]: colors.deepPurple[600],
};
