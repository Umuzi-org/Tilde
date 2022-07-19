import React from "react";

import { Typography, Paper, Grid } from "@material-ui/core";
import {
  ActionReviewedCard,
  ActionCardCompleted,
} from "../../widgets/ActionLogCards";
import Loading from "../../widgets/Loading";

import TodayIcon from "@material-ui/icons/Today";
import { makeStyles } from "@material-ui/core/styles";
import { ACTION_NAMES } from "./constants";

const useStyles = makeStyles((theme) => ({
  calendarIcon: {
    margin: theme.spacing(1),
  },
  dateTypography: {
    marginTop: theme.spacing(2),

    ['@media (max-width:620px)']: { // eslint-disable-line no-useless-computed-key
      fontSize: "1rem",
    }, 
  },

  column: {
    height: "85%", // TODO. Fit viewport
    overflowY: "scroll",
  },
}));

function DayLog({ date, actions, handleClickOpenProjectDetails }) {
  const classes = useStyles();
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
};

export default ({
  orderedDates,
  actionLogByDate,
  handleClickOpenProjectDetails,
  handleScroll,
  anyLoading,
}) => {
  const classes = useStyles();
  return (
    <div className={classes.column} onScroll={handleScroll}>
      <Grid container>
        <Grid>
          <Paper>
            {orderedDates.map((date) => (
              <DayLog
                date={date}
                key={date}
                actions={actionLogByDate[date]}
                handleClickOpenProjectDetails={handleClickOpenProjectDetails}
              />
            ))}

            {anyLoading && <Loading />}
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
};