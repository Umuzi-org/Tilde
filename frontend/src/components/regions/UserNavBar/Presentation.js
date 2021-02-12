import React from "react";

import { Typography, Toolbar, Tooltip } from "@material-ui/core";

import LinkToUserBoard from "../../widgets/LinkToUserBoard";
import LinkToUserActions from "../../widgets/LinkToUserActions";
import GitHubIcon from "@material-ui/icons/GitHub";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  grow: { flexGrow: 1 },
  toolbar: {
    margin: theme.spacing(0.5),
    border: "1px solid grey",
  },
  button: { marginRight: theme.spacing(1) },
  gitHubLink: {
    margin: theme.spacing(1),
  },
}));

export default ({ user, userId, userBoardSelected, UserActionsSelected }) => {
  const classes = useStyles();
  return (
    <React.Fragment>
      <Toolbar variant="dense" className={classes.toolbar}>
        {user && <Typography>{user.email}</Typography>}
        {user && user.githubName && (
          <a
            className={classes.gitHubLink}
            href={`https://github.com/${user.githubName}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            <Tooltip title={user.githubName}>
              <GitHubIcon />
            </Tooltip>
          </a>
        )}

        <div className={classes.grow} />
        <div className={classes.button}>
          <LinkToUserBoard userId={userId} selected={userBoardSelected} />
        </div>
        <div className={classes.button}>
          <LinkToUserActions userId={userId} selected={UserActionsSelected} />
        </div>
      </Toolbar>
    </React.Fragment>
  );
};
