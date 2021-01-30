import React from "react";
import { routes } from "../../routes";

import BaseButtonLink from "./BaseButtonLink";

export default ({ userId, selected, label }) => {
  return (
    <BaseButtonLink
      to={routes.userBoard.route.path.replace(":userId", userId)}
      label={label || "Board"}
      selected={selected}
    />
  );
};
