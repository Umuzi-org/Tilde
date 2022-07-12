import React from "react";
import { makeStyles } from "@material-ui/core";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import Alert from "@material-ui/lab/Alert";
import LockRoundedIcon from "@material-ui/icons/LockRounded";
import Link from "@material-ui/core/Link";
import { Box } from "@material-ui/core";
import Divider from "./Divider";

import { routes } from "../../../routes";

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

const LoginForm = ({
  googleLoginLoading,
  error,
  handleLoginWithGoogle,

  handleInputChange,
  formErrors,
  handleSubmitLoginForm,
  loginFormLoading,
}) => {
  const classes = useStyles();
  // console.log(formErrors);

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

      {formErrors["nonFieldErrors"] && (
        <Alert severity="error" className={classes.alert}>
          {formErrors["nonFieldErrors"]}
        </Alert>
      )}

      <TextField
        margin="normal"
        required
        fullWidth
        id="email"
        label="Email Address"
        name="email"
        autoComplete="email"
        type="email"
        variant="outlined"
        autoFocus
        onChange={handleInputChange}
        error={Boolean(formErrors.email)}
        helperText={formErrors.email}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        name="password"
        label="Password"
        type="password"
        id="password"
        autoComplete="current-password"
        variant="outlined"
        onChange={handleInputChange}
        error={Boolean(formErrors.password)}
        helperText={formErrors.password}
      />
      <Box m={0}>
        <Link
          className={classes.linkStyles}
          underline="always"
          href={routes.forgotPassword.route.path}
        >
          Forgot Password?
        </Link>
      </Box>
      <div>
        <Button
          className={classes.buttonStyle}
          type="submit"
          variant="contained"
          color="primary"
          onClick={handleSubmitLoginForm}
          disabled={loginFormLoading}
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
          type="submit"
          variant="contained"
          color="primary"
          onClick={handleLoginWithGoogle}
          className={classes.buttonStyle}
          disabled={googleLoginLoading}
        >
          Login with Google
        </Button>
      </div>
    </form>
  );
};

export default LoginForm;
