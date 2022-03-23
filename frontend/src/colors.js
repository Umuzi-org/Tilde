import {
  READY,
  BLOCKED,
  COMPLETE,
  IN_REVIEW,
  IN_PROGRESS,
  REVIEW_FEEDBACK,
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
