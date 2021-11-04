import React from "react";
import { routes } from "../../routes";

import BaseButtonLink from "./BaseButtonLink";

export default ({ userId, selected, label }) => {
  return (
    <BaseButtonLink
      to={routes.userDashboard.route.path.replace(":userId", userId)}
      label={label || "Dashboard"}
      selected={selected}
    />
  );
};
