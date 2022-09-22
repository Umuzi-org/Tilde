import React from "react";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import TodayIcon from "@material-ui/icons/Today";
import { makeStyles } from "@material-ui/core/styles";
import {
  ActionReviewedCard,
  ActionCardCompleted,
} from "../../widgets/ActionLogCards";
import { ACTION_NAMES } from "./constants";

const useStyles = makeStyles((theme) => ({
  calendarIcon: {
    margin: theme.spacing(1),
  },
  dateTypography: {
    marginTop: theme.spacing(2),
    ["@media (max-width:620px)"]: {
      // eslint-disable-line no-useless-computed-key
      fontSize: "1rem",
    },
  },
}));

export default function DayLog({
  date,
  actions,
  handleClickOpenProjectDetails,
}) {
  const classes = useStyles();
  console.log(actions);
  return (
    <React.Fragment>
      <Paper>
        <Typography variant="h6" className={classes.dateTypography}>
          <TodayIcon className={classes.calendarIcon} /> {date} [count:{" "}
          {actions.length}]
        </Typography>
      </Paper>
      {actions.map((action) => {
        if (action.actionType === ACTION_NAMES.COMPETENCE_REVIEW_DONE) {
          return (
            <ActionReviewedCard
              review={action}
              key={"review" + action.id}
              handleClickOpenProjectDetails={() =>
                handleClickOpenProjectDetails({ cardId: action.agileCard })
              }
              showReviewer={false}
              showReviewed={true}
            />
          );
        }
        if (action.actionType === ACTION_NAMES.CARD_COMPLETED) {
          return (
            <ActionCardCompleted
              card={action}
              key={"completed" + action.id}
              handleClickOpenProjectDetails={() =>
                handleClickOpenProjectDetails({ cardId: action.id })
              }
            />
          );
        }
        return <Typography>Not Implemented: {action.actionType}</Typography>;
      })}
    </React.Fragment>
  );
}
