import React from "react";
import { routes } from "../../routes";
import BaseButtonLink from "./BaseButtonLink";
import { useStyles } from "./BaseButtonLink";

export function getUrl({ userId }) {
  return routes.userBoard.route.path.replace(":userId", userId);
}
export { useStyles };
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
