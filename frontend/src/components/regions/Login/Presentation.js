import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import { makeStyles } from "@material-ui/core";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import Alert from "@material-ui/lab/Alert";
import LockRoundedIcon from "@material-ui/icons/LockRounded";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import { Box } from "@material-ui/core";
import Divider from "./Divider";
import ForgotPassword from "./ForgotPassword"

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    padding: theme.spacing(2),
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
  alert: {
    margin: theme.spacing(1),
    width: "275px",
  },
  buttonStyle: {
    margin: theme.spacing(1),
    textTransform: "none",
    fontWeight: 600,
    width: "275px",
  },
  linkStyles: {
    overflow: "hidden",
    whiteSpace: "nowrap",
    fontFamily: "Roboto",
  },
  checkBoxStyles: {
    marginLeft: "0",
    width: "20px",
    padding: "0",
  },
}));

const LoginForm = ({ loading, error, handleLoginWithGoogle }) => {
  const classes = useStyles();

  return (
    <form className={classes.root}>
      <Typography variant="h5" style={{ fontWeight: 600 }}>
        Please Login
      </Typography>

      <Alert severity="info" className={classes.alert}>
        Note that this site uses popups for authentication
      </Alert>
      {error && (
        <Alert severity="error" className={classes.alert}>
          ERROR: {error}. You might need to refresh this page to attempt to
          login again
        </Alert>
      )}
      <LockRoundedIcon />
      <TextField label="Email" variant="outlined" type="email" required />
      <TextField label="Password" variant="outlined" type="password" required />
      <Box m={0}>
        <FormControlLabel
          control={
            <Checkbox
              className={classes.checkBoxStyles}
              name="checkedB"
              color="primary"
            />
          }
          label="Remember me"
        />
        <Router>
          <Link to="/forgotPassword" className={classes.linkStyles}>
            Forgot Password?
          </Link>
          <Route exact path="/forgotPassword" component={ForgotPassword} />
        </Router>
      </Box>
      <div>
        <Button
          className={classes.buttonStyle}
          type="submit"
          variant="contained"
          color="default"
        >
          Login
        </Button>
      </div>
      <Box width={200} m={0}>
        <Divider>
          <Typography style={{ fontWeight: 600 }}>OR</Typography>
        </Divider>
      </Box>
      <div>
        <Button
          className={classes.buttonStyle}
          type="submit"
          variant="contained"
          color="primary"
          onClick={handleLoginWithGoogle}
        >
          Login with Google
        </Button>
      </div>
    </form>
  );
};

export default LoginForm;
