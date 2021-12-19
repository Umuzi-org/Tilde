import React from "react";
import { routes } from "../../routes";
import BaseButtonLink from "./BaseButtonLink";
import { makeStyles } from "@material-ui/core/styles";
const useStyles = makeStyles({
  marginsAlignment: {
    marginTop: "8px",
    marginLeft: "16px",
  },
});
export function getUrl({ userId }) {
  return routes.userBoard.route.path.replace(":userId", userId);
}
export default ({ userId, selected, label }) => {
  const classes = useStyles();
  return (
    <BaseButtonLink
      to={getUrl({ userId })}
      label={label || "Board"}
      selected={selected}
      className={classes.marginsAlignment}
    />
  );
};
