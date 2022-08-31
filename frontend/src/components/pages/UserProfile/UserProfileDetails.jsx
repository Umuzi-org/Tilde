import React from "react";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import ButtonGroup from "@material-ui/core/ButtonGroup";
import { makeStyles } from "@material-ui/core/styles";
import GitHubIcon from "@material-ui/icons/GitHub";
import MailIcon from "@material-ui/icons/Mail";
import useMediaQuery from "@material-ui/core/useMediaQuery";
// You can read more about iconify here: https://docs.iconify.design/icon-components/react/
import { Icon } from "@iconify/react";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "block",
    "& > *": {
      margin: theme.spacing(1),
    },
  },
  textStyle: {
    textTransform: "none",
  },
}));

export default function UserProfileDetails() {
  const classes = useStyles();
  const mobile = useMediaQuery("(min-width:600px)");

  return (
    <div className={classes.root}>
      <ButtonGroup
        orientation={`${mobile ? "horizontal" : "vertical"}`}
        color="primary"
        aria-label="text primary button group"
        variant="text"
        size={`${mobile ? "large" : "small"}`}
        disabled
      >
        <Button className={classes.textStyle}>
          <div>
            <div>rocketchat name</div>
            <div>
              <Icon icon="logos:rocket-chat-icon" />
            </div>
          </div>
        </Button>
        <Button className={classes.textStyle}>
          <div>
            <div>github name</div>
            <div>
              <GitHubIcon />
            </div>
          </div>
        </Button>
        <Button className={classes.textStyle}>
          <div>
            <div>email address</div>
            <div>
              <MailIcon />
            </div>
          </div>
        </Button>
      </ButtonGroup>
    </div>
  );
}
