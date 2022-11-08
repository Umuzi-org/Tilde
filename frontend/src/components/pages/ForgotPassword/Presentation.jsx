import React from "react";
import { makeStyles } from "@material-ui/core";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import Alert from "@material-ui/lab/Alert";
import { Link } from "react-router-dom";
import { routes } from "../../../routes";

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

export default ({
  handleSubmit,
  handleInputChange,
  loading,
  formErrors,
  formLastSentTo,
}) => {
  const classes = useStyles();

  return (
    <form className={classes.root}>
      <Typography variant="h5" style={{ fontWeight: 600 }}>
        Reset Password
      </Typography>

      <Alert severity="info" className={classes.alertStyle}>
        Enter the email associated with your account and we will send an email
        with instructions to reset your password
      </Alert>

      {formLastSentTo && (
        <Alert severity="info" className={classes.alertStyle}>
          Password reset email has been sent to {formLastSentTo}. Please check
          your inbox. If you typed in the wrong email address then you can use
          the form below to send another email.
        </Alert>
      )}

      {formErrors.nonFieldErrors && (
        <Alert severity="error" className={classes.alertStyle}>
          <Typography>{formErrors.nonFieldErrors}</Typography>
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
        onChange={handleInputChange}
        autoFocus
        error={Boolean(formErrors.email)}
        helperText={formErrors.email}
        variant="outlined"
      />

      <div>
        <Link to={routes.login.route.path}>
          <Button
            className={classes.buttonStyle}
            variant="contained"
            color="secondary"
          >
            back
          </Button>
        </Link>

        <Button
          className={classes.buttonStyle}
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading}
          onClick={handleSubmit}
        >
          submit
        </Button>
      </div>
    </form>
  );
};
