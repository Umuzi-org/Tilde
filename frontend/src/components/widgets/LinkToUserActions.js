import React from "react";
import { routes } from "../../routes";
import BaseButtonLink from "./BaseButtonLink";

export function getUrl({ userId }) {
  return routes.userActions.route.path.replace(":userId", userId);
}

export default ({ userId, selected }) => {
  return (
    <BaseButtonLink
      to={getUrl}
      label="Actions"
      selected={selected}
    />
  );
};
