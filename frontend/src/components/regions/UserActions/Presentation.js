import React from "react";

import { Typography, Paper, Grid } from "@mui/material";
import {
  ActionReviewedCard,
  ActionCardCompleted,
} from "../../widgets/ActionLogCards";
import Loading from "../../widgets/Loading";

import TodayIcon from "@mui/icons-material/Today";
import { makeStyles } from "@mui/material/styles";
import { ACTION_NAMES } from "./constants";

const useStyles = makeStyles((theme) => ({
  calendarIcon: {
    margin: theme.spacing(1),
  },
  dateTypography: {
    marginTop: theme.spacing(2),
    // marginLeft: theme.spacing(2),
    // marginTop: theme.spacing(0),
    // paddingTop: theme.spacing(0),
  },

  column: {
    height: "85%", // TODO. Fit viewport
    overflowY: "scroll",
  },
}));

const DayLog = ({ date, actions, handleClickOpenProjectDetails }) => {
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

// {actionLog.map((action) => {

//   })}
