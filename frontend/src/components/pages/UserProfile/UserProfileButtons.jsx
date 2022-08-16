import React from "react";
import Button from "@material-ui/core/Button";
import ButtonGroup from "@material-ui/core/ButtonGroup";
import { makeStyles } from "@material-ui/core/styles";
import GitHubIcon from "@material-ui/icons/GitHub";
import MailIcon from "@material-ui/icons/Mail";
import useMediaQuery from "@material-ui/core/useMediaQuery";
// You can read more about iconify here: https://docs.iconify.design/icon-components/react/
import { Icon } from "@iconify/react";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    "& > *": {
      margin: theme.spacing(1),
    },
  },
  textStyle: {
    textTransform: "none",
  },
}));

export default function UserProfileButton() {
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
      >
        <div>
          <Button className={classes.textStyle}>
            {/* <Icon icon="logos:rocket-chat-icon" /> */}
            Sbonelo
          </Button>
          <Button className={classes.textStyle}>
            {" "}
            {/* <GitHubIcon /> */}
            Sbonelo01
          </Button>
          <Button className={classes.textStyle}>
            {/* <MailIcon /> */}
            sbonelo.mkhize@umuzi.org
          </Button>
        </div>
      </ButtonGroup>
    </div>
  );
}
