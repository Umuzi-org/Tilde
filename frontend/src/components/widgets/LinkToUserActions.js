import React from "react";
import { routes } from "../../routes";
import BaseButtonLink from "./BaseButtonLink";

export default ({ userId, selected }) => {
  return (
    <BaseButtonLink
      to={routes.userActions.route.path.replace(":userId", userId)}
      label="Actions"
      selected={selected}
    />
  );
};
