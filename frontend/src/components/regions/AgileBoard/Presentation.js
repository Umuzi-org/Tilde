import React from "react";

import { makeStyles } from "@mui/material/styles";

import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";

import AgileCard from "./AgileCard";
import Loading from "../../widgets/Loading";

// import MarkSingleCardAttendanceModal from "../MarkSingleCardAttendanceModal";
import { Divider } from "@mui/material";

const useStyles = makeStyles((theme) => ({
  grid: {
    display: "nowrap",
    "& > *": {
      margin: theme.spacing(1),
      width: theme.spacing(35),
      // height: theme.spacing(100),
      // height: `calc(100% - ${0}px)`,
      // height: "calc(100vh - 20rem)",
    },
  },

  paper: {
    height: "calc(100vh - 6rem)",
  },

  column: {
    height: "calc(100% - 2.5rem)",
    overflowY: "scroll",
  },
}));

export default ({
  board,
  cards,
  handleColumnScroll,
  userId,
  viewedUser,
  columnsLoading,
}) => {
  const classes = useStyles();
  return (
    <React.Fragment>
      {/* <Typography>{user.email}</Typography> */}
      <Grid container wrap="nowrap">
        {board.map((column) => {
          return (
            <React.Fragment key={column.label}>
              <Grid
                item
                xs={"auto"}
                className={classes.grid}
                key={column.label}
              >
                <Paper elevation={3} className={classes.paper}>
                  <Typography variant="h5" align="center">
                    {column.label}
                  </Typography>
                  <div
                    className={classes.column}
                    onScroll={handleColumnScroll({ column })}
                  >
                    {column.cards.map((cardId, index) => {
                      return (
                        <AgileCard
                          key={cardId}
                          card={cards[cardId]}
                          filterUserId={userId}
                          viewedUser={viewedUser}
                        />
                      );
                    })}
                    {columnsLoading.includes(column.label) && <Loading />}
                    <Divider />
                  </div>
                </Paper>
              </Grid>
            </React.Fragment>
          );
        })}
      </Grid>
    </React.Fragment>
  );
};
