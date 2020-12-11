import React from "react";
import {routes} from "../../routes";
import BaseButtonLink from "./BaseButtonLink"

export default ({userId,selected}) => {

    return <BaseButtonLink
    to={routes.userStats.route.path.replace(
        ":userId",
        userId
        )}
    label="Stats"
    selected={selected}
/>



}