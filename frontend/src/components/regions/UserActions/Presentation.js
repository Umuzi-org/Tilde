import React from "react";

import { Typography, Paper, Grid } from "@material-ui/core";
import ActionReviewedCard from "../../widgets/ActionReviewedCard";
import TodayIcon from "@material-ui/icons/Today";
import { makeStyles } from "@material-ui/core/styles";

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
        if (action.actionType === "Review Done") {
          return (
            <ActionReviewedCard
              review={action}
              key={action.id}
              handleClickOpenProjectDetails={() =>
                handleClickOpenProjectDetails({ cardId: action.agileCard })
              }
              showReviewer={false}
              showReviewed={true}
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
}) => {
  return (
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
        </Paper>
      </Grid>
    </Grid>
  );
};

// {actionLog.map((action) => {

//   })}
