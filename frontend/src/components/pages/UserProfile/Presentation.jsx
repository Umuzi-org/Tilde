// import React from "react";

// export default function Presentation() {
//   return <div>TODO</div>;
// };

import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Avatar from "@material-ui/core/Avatar";
// import Typography from "@material-ui/core"

const useStyles = makeStyles((theme) => ({
  root: {
    maxHeight: "90vh",
    maxWidth: "90vw",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  paper: {
    padding: theme.spacing(0),
    textAlign: "center",
    color: theme.palette.text.secondary,
    height: "40vh",
  },
}));

export default function UserProfile() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Grid container spacing={0} justifyContent="center" alignItems="center">
        <Grid item xs={12} sx={12} md={6} lg={6}>
          <Paper className={classes.paper}>
            <Avatar variant="square" style={{ width: "100%", height: "100%" }}>
              SD
            </Avatar>
          </Paper>
        </Grid>
        <Grid item xs={12} sx={12} md={6} lg={6}>
          <Paper className={classes.paper}>Details</Paper>
        </Grid>
      </Grid>
    </div>
  );
}
