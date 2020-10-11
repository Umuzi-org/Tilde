import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";

const useStyles = makeStyles({
  root: {
    minWidth: 275,
    marginLeft: "450px",
    marginTop: "100px",
    width: "400px",
    height: "200px",
  },
  button: {
    marginLeft: "100px",
    marginTop: "5px",
  },
});

export default ({ loading, error, handleLoginWithGoogle }) => {
  const classes = useStyles();

  return (
    <Card className={classes.root}>
      <CardContent>
        <Typography>
          Please log in. Use a Gmail registered account.
        </Typography>

        <br />
        <Typography>
          Note that this site uses popups for authentication.
        </Typography>

        {error && (
          <Typography>
            ERROR: {error}. You might need to refresh this page to attempt to
            login again
          </Typography>
        )}
      </CardContent>
      <CardActions>
        <Button
          className={classes.button}
          variant="contained"
          onClick={handleLoginWithGoogle}
        >
          Login with Google
        </Button>
      </CardActions>
    </Card>
  );
};

// TODO: make this look better needsissue
