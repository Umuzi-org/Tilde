import React from "react";
import { routes } from "../../routes";

import BaseButtonLink from "./BaseButtonLink";

export function getUrl({ userId }) {
  return routes.userBoard.route.path.replace(":userId", userId);
}

export default ({ userId, selected, label }) => {
  return (
    <BaseButtonLink
      to={getUrl({ userId })}
      label={label || "Board"}
      selected={selected}
    />
  );
};
