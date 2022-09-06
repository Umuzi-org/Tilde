import React from "react";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import TodayIcon from "@material-ui/icons/Today";
import { makeStyles } from "@material-ui/core/styles";
import {
  ActionReviewedCard,
  ActionCardCompleted,
} from "../../widgets/ActionLogCards";
<<<<<<<< HEAD:frontend/src/components/regions/UserActions/Presentation.jsx
import Loading from "../../widgets/Loading";
import UserBurnDownChart from "./UserBurndownStats";

import TodayIcon from "@material-ui/icons/Today";
import { makeStyles } from "@material-ui/core/styles";
========
>>>>>>>> develop:frontend/src/components/regions/UserActions/DayLog.jsx
import { ACTION_NAMES } from "./constants";

const useStyles = makeStyles((theme) => ({
  calendarIcon: {
    margin: theme.spacing(1),
  },
  dateTypography: {
    marginTop: theme.spacing(2),
<<<<<<<< HEAD:frontend/src/components/regions/UserActions/Presentation.jsx
    // eslint-disable-next-line
    ["@media (max-width:620px)"]: {
      // eslint-disable-line no-useless-computed-key
      fontSize: "1rem",
    },
    // marginLeft: theme.spacing(2),
    // marginTop: theme.spacing(0),
    // paddingTop: theme.spacing(0),
  },
  column: {
    height: "85%", // TODO. Fit viewport
    overflowY: "scroll",
========
    ["@media (max-width:620px)"]: {// eslint-disable-line no-useless-computed-key
      fontSize: "1rem",
    },
>>>>>>>> develop:frontend/src/components/regions/UserActions/DayLog.jsx
  },
}));

export default function DayLog({
  date,
  actions,
  handleClickOpenProjectDetails,
}) {
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
<<<<<<<< HEAD:frontend/src/components/regions/UserActions/Presentation.jsx
};

export default ({
  orderedDates,
  actionLogByDate,
  handleClickOpenProjectDetails,
  handleScroll,
  anyLoading,
  currentUserBurndownStats,
}) => {
  const classes = useStyles();
  return (
    <div className={classes.column} onScroll={handleScroll}>
      <Grid container>
        <Grid item xs={12}>
          {currentUserBurndownStats && (
            <Grid>
              <Paper className={classes.paper}>
                <UserBurnDownChart
                  burnDownSnapshots={currentUserBurndownStats}
                />
              </Paper>
            </Grid>
          )}
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
========
}
>>>>>>>> develop:frontend/src/components/regions/UserActions/DayLog.jsx
