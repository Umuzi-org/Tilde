import React from "react";
import { routes } from "../../routes";

import BaseButtonLink from "./BaseButtonLink";

export function getUrl({ userId }) {
  return routes.userDashboard.route.path.replace(":userId", userId);
}
export default ({ userId, selected, label }) => {
  return (
    <BaseButtonLink
      to={getUrl}
      label={label || "Dashboard"}
      selected={selected}
    />
  );
};
