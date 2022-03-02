import React from "react";
import { BrowserRouter as Router, Link } from "react-router-dom";
import { makeStyles } from "@material-ui/core";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import Alert from "@material-ui/lab/Alert";
import { routes } from "../../../../routes";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    padding: theme.spacing(1),
    height: "100vh",
    overflow: "hidden",

    "& .MuiTextField-root": {
      margin: theme.spacing(1),
      width: "300px",
    },
    "& .MuiButtonBase-root": {
      margin: theme.spacing(2),
    },
  },
  alertStyle: {
    margin: theme.spacing(1),
    width: "275px",
  },
  buttonStyle: {
    width: "134px",
  },
}));

export default () => {
  const classes = useStyles();

  return (
    <form className={classes.root}>
      <Typography variant="h5" style={{ fontWeight: 600 }}>
        Forgot Password
      </Typography>

      <Alert severity="info" className={classes.alertStyle}>
        Enter the email associated with your account and we will send an email
        with instructions to reset your password
      </Alert>

      <TextField label="Email" variant="outlined" type="email" required />

      <div>
        <Router to={routes.loginRedirect.route.path}>
          <Button
            className={classes.buttonStyle}
            type="submit"
            variant="contained"
            color="secondary"
            component={Link}
          >
            back
          </Button>
        </Router>
        <Button
          className={classes.buttonStyle}
          type="submit"
          variant="contained"
          color="primary"
        >
          submit
        </Button>
      </div>
    </form>
  );
};
