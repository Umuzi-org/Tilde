import React from "react";
import { Link } from "react-router-dom";
import {routes} from "../../routes";

import {
    Button,
  } from "@material-ui/core";

export default ({userId}) => {
    return (

        <Link
        to={routes.userBoard.route.path.replace(
          ":userId",
          userId
        )}
      >
        <Button size="small" variant="outlined">
          Board
        </Button>
      </Link>
    )
}