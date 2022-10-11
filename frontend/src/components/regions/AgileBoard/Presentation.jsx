import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import AgileCard from "./AgileCard";
import Loading from "../../widgets/Loading";
import Button from "@material-ui/core/Button";
import Divider from "@material-ui/core/Divider";

const useStyles = makeStyles((theme) => ({
  grid: {
    display: "nowrap",
    "& > *": {
      margin: theme.spacing(1),
      width: theme.spacing(35),
    },
  },
  paper: {
    height: "calc(100vh - 6rem)",
  },
  column: {
    height: "calc(100% - 2.5rem)",
    overflowY: "scroll",
  },
  typography: {
    margin: "auto",
    position: "relative",
    top: 4,
  },
}));

export default function Presentation({
  board,
  cards,
  handleColumnScroll,
  userId,
  viewedUser,
  columnsLoading,
  loadMoreCards,
}) {
  const classes = useStyles();
  return (
    <React.Fragment>
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
                  <Typography
                    variant="h5"
                    align="center"
                    className={classes.typography}
                  >
                    {column.label} ({column.totalCards})
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
                    {columnsLoading.includes(column.label) ? (
                      <Loading />
                    ) : (
                      <Button onClick={loadMoreCards({ column })}>
                        Load more
                      </Button>
                    )}
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
}
